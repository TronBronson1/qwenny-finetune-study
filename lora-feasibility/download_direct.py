"""Direct public HTTPS fallback; records immutable revision and validates LFS SHA256."""
import concurrent.futures, hashlib, json, pathlib, time, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
REV='c202236235762e1c871ad0ccb60c8ee5ba337b9a'
DEST=ROOT/'checkpoint'/REV

def main():
    DEST.mkdir(parents=True,exist_ok=True)
    manifest=json.load(urllib.request.urlopen(f'https://huggingface.co/api/models/Qwen/Qwen3.5-9B/revision/{REV}?blobs=true',timeout=60))
    assert manifest['sha']==REV
    (DEST/'source-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    files=[f for f in manifest['siblings'] if f['rfilename'].endswith(('.json','.txt','.jinja','.safetensors')) or f['rfilename']=='LICENSE']
    def fetch(info):
        name=info['rfilename']; target=DEST/name; part=target.with_suffix(target.suffix+'.part')
        expected=info.get('lfs',{}).get('sha256'); size=info.get('size')
        if target.exists() and target.stat().st_size==size:
            if not expected or hashlib.file_digest(target.open('rb'),'sha256').hexdigest()==expected:
                print(name,'already verified',flush=True); return
        for attempt in range(3):
            offset=part.stat().st_size if part.exists() else 0
            url=f'https://huggingface.co/Qwen/Qwen3.5-9B/resolve/{REV}/{name}?direct=1'
            try:
                req=urllib.request.Request(url,headers={'Range':f'bytes={offset}-'} if offset else {})
                with urllib.request.urlopen(req,timeout=60) as response:
                    if offset and response.status==206:
                        assert response.headers.get('Content-Range','').startswith(f'bytes {offset}-'), 'Incorrect resume offset'
                    if offset and response.status!=206: offset=0
                    with part.open('ab' if offset else 'wb') as f:
                        printed=offset
                        while block:=response.read(8*1024*1024):
                            f.write(block); offset+=len(block)
                            if offset-printed>=256*1024**2:
                                print(name,offset,'/',size,flush=True); printed=offset
                assert part.stat().st_size==size,(name,part.stat().st_size,size)
                if expected:
                    with part.open('rb') as f: actual=hashlib.file_digest(f,'sha256').hexdigest()
                    assert actual==expected,(name,'SHA256 mismatch')
                part.replace(target); print(name,'verified',flush=True); return
            except Exception as e:
                print(name,'attempt',attempt+1,type(e).__name__,str(e)[:120],flush=True)
                if attempt==2: raise
                time.sleep(2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(fetch,files))
    (DEST/'download-complete.json').write_text(json.dumps({'revision':REV,'verified_files':[f['rfilename'] for f in files]},indent=2),encoding='utf-8')
    print('COMPLETE',DEST,flush=True)

if __name__=='__main__': main()
