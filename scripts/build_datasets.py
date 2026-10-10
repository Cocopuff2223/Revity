"""Generate deterministic, programmatically labeled starter data; no model required."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random

SEED = 20261010
TASKS = ('arithmetic', 'linear_equations', 'sorting', 'unit_conversion', 'word_count', 'boolean_logic')
SPLITS = {'train': 1600, 'validation': 200, 'test': 200}  # Per task.


def example(task, rng):
    if task == 'arithmetic':
        a, b, c = (rng.randint(-10000, 10000) for _ in range(3))
        prompt, answer = f'Calculate ({a} + {b}) * {c}. Return only the integer.', str((a + b) * c)
    elif task == 'linear_equations':
        a, x, b = rng.randint(1, 99), rng.randint(-10000, 10000), rng.randint(-999, 999)
        prompt, answer = f'Solve {a} * x + ({b}) = {a*x+b}. Return only the integer x.', str(x)
    elif task == 'sorting':
        numbers = [rng.randint(-999, 999) for _ in range(rng.randint(4, 12))]
        prompt = f'Sort these integers in ascending order. Return only a JSON array: {json.dumps(numbers)}'
        answer = json.dumps(sorted(numbers))
    elif task == 'unit_conversion':
        source, target, scale = rng.choice([('kilometers', 'meters', 1000), ('meters', 'centimeters', 100), ('hours', 'minutes', 60), ('minutes', 'seconds', 60)])
        number = rng.randint(1, 100000)
        prompt, answer = f'Convert {number} {source} to {target}. Return only the integer.', str(number * scale)
    elif task == 'word_count':
        words = [rng.choice(('sun', 'river', 'tree', 'cloud', 'stone', 'bird', 'moon', 'rain')) for _ in range(rng.randint(8, 30))]
        target = rng.choice(words)
        prompt = f'Count exact occurrences of "{target}" in this space-separated text. Return only the integer: {" ".join(words)}'
        answer = str(words.count(target))
    else:
        a, b, c, d = (rng.randint(-1000, 1000) for _ in range(4))
        op = rng.choice(('AND', 'OR'))
        prompt = f'Evaluate ({a} < {b}) {op} ({c} >= {d}). Return only true or false.'
        answer = str((a < b and c >= d) if op == 'AND' else (a < b or c >= d)).lower()
    return prompt, answer


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError('Output directory must be empty to avoid overwriting existing data.')
    rng = random.Random(SEED)
    seen = set()
    manifest = {'version': '0.1.0', 'seed': SEED, 'provenance': 'Programmatically generated; no external datasets or model outputs.', 'files': {}}
    for split, count in SPLITS.items():
        rows = []
        for task in TASKS:
            for _ in range(count):
                while True:
                    prompt, answer = example(task, rng)
                    identity = hashlib.sha256(prompt.encode()).hexdigest()
                    if identity not in seen:
                        seen.add(identity)
                        break
                rows.append({'id': identity, 'task': task, 'split': split, 'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': answer}]})
        rng.shuffle(rows)
        path = output / f'{split}.jsonl'
        path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8')
        manifest['files'][path.name] = {'rows': len(rows), 'tasks': dict(sorted(Counter(row['task'] for row in rows).items())), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2))
