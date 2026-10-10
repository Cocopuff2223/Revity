"""Run real inference and save observed responses; this is not a benchmark."""
import json
from pathlib import Path
import platform
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from revity.chat import Chat

if __name__ == '__main__':
    started = time.monotonic()
    chat = Chat()
    results = []
    for prompt in ('What is 2 + 2? Return only the number.', 'Explain what a solar panel does in two sentences.', 'Say hello in French.'):
        tick = time.monotonic()
        answer = chat.reply([{'role': 'user', 'content': prompt}], max_new_tokens=128)
        if not answer:
            raise RuntimeError('Model produced an empty reply')
        results.append({'prompt': prompt, 'response': answer, 'seconds': round(time.monotonic() - tick, 3)})
    report = {'status': 'real_inference_completed', 'model': 'Qwen/Qwen3-0.6B', 'revision': 'c1899de289a04d12100db370d81485cdf75e47ca', 'fine_tuned': False, 'platform': platform.platform(), 'python': platform.python_version(), 'device': 'cpu', 'decoding': {'do_sample': False, 'enable_thinking': False, 'max_new_tokens': 128}, 'results': results, 'seconds_including_load': round(time.monotonic() - started, 3), 'limitation': 'Nonempty-output smoke checks only; no broad accuracy or benchmark claim.'}
    (Path(__file__).resolve().parent.parent / 'docs/SMOKE_RESULTS.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
