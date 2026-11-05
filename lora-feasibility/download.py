"""Fetch the immutable upstream checkpoint into this experiment's own cache."""
from pathlib import Path
import os
os.environ['HF_HUB_DISABLE_XET']='1'
os.environ['HF_HUB_DOWNLOAD_TIMEOUT']='60'
from huggingface_hub import snapshot_download

if __name__ == '__main__':
    print(snapshot_download('Qwen/Qwen3.5-9B',
        revision='c202236235762e1c871ad0ccb60c8ee5ba337b9a',
        cache_dir=Path(__file__).resolve().parent/'hf-cache',
        allow_patterns=['*.json','*.safetensors','*.jinja','*.txt','LICENSE'],
        max_workers=2))
