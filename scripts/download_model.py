"""Download original Apache-2.0 Qwen3-0.6B weights at an immutable revision."""
import os
os.environ.setdefault('HF_HUB_DISABLE_XET', '1')
from pathlib import Path
from huggingface_hub import snapshot_download

MODEL = 'Qwen/Qwen3-0.6B'
REVISION = 'c1899de289a04d12100db370d81485cdf75e47ca'

if __name__ == '__main__':
    snapshot_download(MODEL, revision=REVISION, local_dir=Path(__file__).resolve().parent.parent / 'models/Qwen3-0.6B', allow_patterns=['*.json', '*.safetensors', '*.txt', '*.jinja', '*.md', 'LICENSE', 'NOTICE'], max_workers=2)
