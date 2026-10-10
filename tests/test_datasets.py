import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest

from scripts.build_datasets import build, SPLITS, TASKS
from scripts.evaluate import score


class DatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.manifest = build(cls.root / 'first')
        cls.rows = {split: [json.loads(line) for line in (cls.root / 'first' / f'{split}.jsonl').read_text().splitlines()] for split in SPLITS}

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_reproducible(self):
        build(self.root / 'second')
        for path in (self.root / 'first').iterdir():
            self.assertEqual(path.read_bytes(), (self.root / 'second' / path.name).read_bytes())

    def test_split_integrity(self):
        seen = set()
        for split, rows in self.rows.items():
            self.assertEqual(len(rows), SPLITS[split] * len(TASKS))
            for task in TASKS:
                self.assertEqual(sum(row['task'] == task for row in rows), SPLITS[split])
            for row in rows:
                self.assertEqual(row['split'], split)
                self.assertEqual([m['role'] for m in row['messages']], ['user', 'assistant'])
                self.assertEqual(row['id'], hashlib.sha256(row['messages'][0]['content'].encode()).hexdigest())
                self.assertNotIn(row['id'], seen)
                seen.add(row['id'])
            path = self.root / 'first' / f'{split}.jsonl'
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), self.manifest['files'][path.name]['sha256'])

    def test_answers_independently_from_prompts(self):
        for rows in self.rows.values():
            for row in rows:
                prompt, answer = (m['content'] for m in row['messages'])
                task = row['task']
                if task == 'arithmetic':
                    a, b, c = map(int, re.findall(r'-?\d+', prompt))
                    self.assertEqual(int(answer), a*c + b*c)
                elif task == 'linear_equations':
                    a, b, result = map(int, re.findall(r'-?\d+', prompt))
                    self.assertEqual(a*int(answer) + b, result)
                elif task == 'sorting':
                    values = json.loads(prompt.split(': ', 1)[1])
                    actual = json.loads(answer)
                    self.assertCountEqual(values, actual)
                    self.assertTrue(all(a <= b for a, b in zip(actual, actual[1:])))
                elif task == 'unit_conversion':
                    match = re.fullmatch(r'Convert (\d+) (\w+) to (\w+). Return only the integer.', prompt)
                    value, source, target = match.groups()
                    factor = {('kilometers', 'meters'): 1000, ('meters', 'centimeters'): 100, ('hours', 'minutes'): 60, ('minutes', 'seconds'): 60}[source, target]
                    self.assertEqual(int(answer) // factor, int(value))
                    self.assertEqual(int(answer) % factor, 0)
                elif task == 'word_count':
                    target = prompt.split('"')[1]
                    text = prompt.split(': ', 1)[1]
                    self.assertEqual(int(answer), sum(word == target for word in text.split()))
                else:
                    a, b, c, d = map(int, re.findall(r'-?\d+', prompt))
                    truths = [a < b, c >= d]
                    expected = all(truths) if ' AND ' in prompt else any(truths)
                    self.assertEqual(answer, str(expected).lower())

    def test_refuses_overwrite(self):
        with self.assertRaises(ValueError):
            build(self.root / 'first')

    def predictions(self, rows, name):
        path = self.root / name
        path.write_text(''.join(json.dumps(row) + '\n' for row in rows))
        return path

    def test_scorer_correct_and_incorrect(self):
        rows = [{'id': row['id'], 'prediction': row['messages'][1]['content']} for row in self.rows['test']]
        # Reference answers exercise the scorer only; these are NOT model results.
        predictions = self.predictions(rows, 'reference.jsonl')
        result = score(self.root / 'first/test.jsonl', predictions)
        self.assertEqual(result['correct'], 1200)
        rows[0]['prediction'] = 'intentionally incorrect'
        result = score(self.root / 'first/test.jsonl', self.predictions(rows, 'wrong.jsonl'))
        self.assertEqual(result['correct'], 1199)

    def test_scorer_rejects_incomplete_duplicate_extra_and_training(self):
        rows = [{'id': row['id'], 'prediction': '0'} for row in self.rows['test']]
        for index, bad in enumerate((rows[:-1], rows + [rows[0]], rows + [{'id': 'unexpected', 'prediction': '0'}])):
            with self.assertRaises(ValueError):
                score(self.root / 'first/test.jsonl', self.predictions(bad, f'bad{index}.jsonl'))
        with self.assertRaises(ValueError):
            score(self.root / 'first/train.jsonl', self.predictions(rows, 'train.jsonl'))


if __name__ == '__main__':
    unittest.main()
