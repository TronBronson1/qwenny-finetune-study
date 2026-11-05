"""Execute saved first attempts only after explicit hash-bound source inspection."""
import ast,json,pathlib,sys
from prepare_study import HERE,DATA,read,dump,sha
from s009_bindings import verify_frozen
from suite_scorer import score
def main():
    verify_frozen()
    binding=read(HERE/'measurement-supplement-binding.json')
    assert sha(HERE/'requirement-catalog.json')==binding['requirement_catalog_sha256']
    generation=read(HERE/'inference-001/report.json'); assert generation['status'] in ('completed','stopped-budget')
    reviews=read(HERE/'source-reviews.json')['reviews']
    out=HERE/'scoring-001'; assert not out.exists(); out.mkdir()
    results=[]
    for generated in generation['completed']:
        ident,label=generated['task'],generated['variant']; key=ident+'/'+label
        source=HERE/'inference-001'/ident/label/'test_candidate.py'
        item=dict(task=ident,split=generated['split'],variant=label,terminated=generated['terminated'],truncated=generated['truncated'],format_valid=generated['python_blocks']==1)
        results.append(item)
        if not source.exists():
            item.update(reference_valid=False,execution='no-single-python-block'); continue
        review=reviews[key]; assert review['source_sha256']==sha(source),key
        item['source_sha256']=sha(source)
        if not review['approved_for_isolated_execution']:
            item.update(reference_valid=False,execution='excluded-after-source-inspection',review_reason=review['reason']); continue
        try: ast.parse(source.read_text(encoding='utf-8'))
        except SyntaxError as e:
            item.update(reference_valid=False,execution='syntax-invalid',syntax_error=str(e)); continue
        task=DATA/'tasks'/generated['split']/ident
        result=score(source,task,out/ident/label,sys.executable,review)
        item.update(execution='completed',raw_reference_valid=result['variants'][0]['reference_valid'],reference_valid=result['reference_valid'] and generated['terminated'] and item['format_valid'],candidate_mutant_witnesses=result['eligible_candidate_mutants'],designated_mutants=result['designated_mutants'],summary_sha256=sha(out/ident/label/'summary.json'))
        dump(out/'progress.json',dict(completed=len(results),total=len(generation['completed'])))
        print(json.dumps(item),flush=True)
    dump(out/'summary.json',dict(status='executed-awaiting-witness-and-requirement-review',results=results,source_reviews_sha256=sha(HERE/'source-reviews.json'),scorer_sha256=sha(HERE/'suite_scorer.py'),script_sha256=sha(pathlib.Path(__file__))))
if __name__=='__main__':main()
