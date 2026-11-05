$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$python312 = 'C:\Users\jalar\AppData\Local\Python\pythoncore-3.12-64\python.exe'
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    & $python312 -m venv .venv
    if ($LASTEXITCODE) { throw 'Virtual environment creation failed' }
}
& .\.venv\Scripts\python.exe -m pip install torch==2.14.1 --index-url https://download.pytorch.org/whl/cu126
if ($LASTEXITCODE) { throw 'PyTorch installation failed' }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE) { throw 'Training library installation failed' }
& .\.venv\Scripts\python.exe -m pip check
if ($LASTEXITCODE) { throw 'Dependency validation failed' }
& .\.venv\Scripts\python.exe -m pip freeze | Set-Content -Encoding utf8 packages.lock.txt
& .\.venv\Scripts\python.exe -c "import torch,transformers,peft,bitsandbytes; from transformers import Qwen3_5ForConditionalGeneration; print(torch.__version__, torch.version.cuda, torch.cuda.is_available()); print(torch.cuda.get_device_name(0)); print(torch.cuda.is_bf16_supported())"
if ($LASTEXITCODE) { throw 'CUDA/import compatibility check failed' }
