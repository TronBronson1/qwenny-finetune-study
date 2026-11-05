"""Small synthetic NF4/BF16 CUDA check; not a Qwen training/quality result."""
import json, pathlib
import torch
import bitsandbytes as bnb

torch.manual_seed(42)
base=bnb.nn.Linear4bit(64,64,bias=False,compute_dtype=torch.bfloat16,compress_statistics=True,quant_type='nf4').to('cuda')
base.weight.requires_grad_(False)
x=torch.randn(1,128,64,device='cuda',dtype=torch.bfloat16,requires_grad=True)
a=torch.nn.Parameter(torch.randn(64,4,device='cuda',dtype=torch.float32)*0.01)
b=torch.nn.Parameter(torch.zeros(4,64,device='cuda',dtype=torch.float32))
optimizer=torch.optim.AdamW([a,b],lr=1e-4)
with torch.autocast('cuda',dtype=torch.bfloat16):
    loss=(base(x)+x@a@b).float().square().mean()
loss.backward()
assert torch.isfinite(loss) and torch.isfinite(x.grad).all()
assert base.weight.grad is None
assert torch.isfinite(b.grad).all() and torch.count_nonzero(b.grad)>0
before=b.detach().clone(); optimizer.step()
assert not torch.equal(before,b)
report={'status':'passed','scope':'synthetic Linear4bit only; no Qwen weights', 'loss':loss.item(),'torch':torch.__version__,'cuda':torch.version.cuda,'gpu':torch.cuda.get_device_name(0),'peak_allocated_bytes':torch.cuda.max_memory_allocated()}
pathlib.Path(__file__).with_name('kernel-preflight.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
