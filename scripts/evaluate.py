"""Score saved predictions against a generated evaluation split; does not run a model."""
import argparse
from collections import Counter
import json
from pathlib import Path


def score(dataset, predictions):
    rows = [json.loads(line) for line in Path(dataset).read_text().splitlines()]
    if not rows or any(row['split'] not in ('test', 'validation') for row in rows):
        raise ValueError('Use a nonempty validation or test split, never training data.')
    expected = {row['id'] for row in rows}
    if len(expected) != len(rows):
        raise ValueError('Dataset contains duplicate IDs.')
    supplied = {}
    for line in Path(predictions).read_text().splitlines():
        row = json.loads(line)
        if row['id'] in supplied or not isinstance(row['prediction'], str):
            raise ValueError('Predictions must have unique IDs and string answers.')
        supplied[row['id']] = row['prediction']
    if set(supplied) != expected:
        raise ValueError('Provide exactly one prediction for every dataset ID, with no extra IDs.')
    total, correct = Counter(), Counter()
    for row in rows:
        task = row['task']
        total[task] += 1
        correct[task] += supplied[row['id']].strip() == row['messages'][1]['content'].strip()
    return {'metric': 'exact_match_after_trimming_whitespace', 'examples': len(rows), 'correct': sum(correct.values()), 'accuracy': sum(correct.values()) / len(rows), 'by_task': {task: {'examples': total[task], 'correct': correct[task], 'accuracy': correct[task] / total[task]} for task in sorted(total)}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--predictions', required=True, help='JSONL records containing id and prediction strings.')
    args = parser.parse_args()
    print(json.dumps(score(args.dataset, args.predictions), indent=2))
