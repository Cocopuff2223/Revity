"""Local-only Qwen chat. Model files must be downloaded first."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = ROOT / 'models' / 'Qwen3-0.6B'


class Chat:
    def __init__(self, model_path=DEFAULT_MODEL):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        torch.set_num_threads(4)
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(str(model_path), local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(str(model_path), local_files_only=True, torch_dtype=torch.float32)
        self.model.eval()

    def reply(self, messages, max_new_tokens=256):
        if not isinstance(messages, list) or not 1 <= len(messages) <= 21 or len(messages) % 2 != 1:
            raise ValueError('Supply up to 10 complete turns followed by a user message.')
        for i, message in enumerate(messages):
            role = 'user' if i % 2 == 0 else 'assistant'
            if not isinstance(message, dict) or message.get('role') != role or not isinstance(message.get('content'), str) or not message['content'].strip() or len(message['content']) > 8000:
                raise ValueError('Messages must alternate user/assistant and contain 1–8000 characters.')
        if not isinstance(max_new_tokens, int) or not 1 <= max_new_tokens <= 512:
            raise ValueError('max_new_tokens must be between 1 and 512.')
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        inputs = self.tokenizer(prompt, return_tensors='pt')
        if inputs['input_ids'].shape[1] > 4096:
            raise ValueError('Conversation exceeds 4096 tokens. Start a new chat or shorten your message.')
        with self.torch.inference_mode():
            output = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=self.tokenizer.eos_token_id)
        generated = output[0, inputs['input_ids'].shape[1]:]
        return self.tokenizer.decode(generated, skip_special_tokens=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, default=DEFAULT_MODEL)
    parser.add_argument('--prompt', help='Generate one response and exit.')
    args = parser.parse_args()
    chat = Chat(args.model)
    if args.prompt:
        print(chat.reply([{'role': 'user', 'content': args.prompt}]))
        return
    print('Revity preview · Qwen3-0.6B · /quit to exit · /reset for a new chat')
    history = []
    while True:
        try:
            prompt = input('You: ').strip()
        except (EOFError, KeyboardInterrupt):
            break
        if prompt == '/quit':
            break
        if prompt == '/reset':
            history = []
            continue
        if not prompt:
            continue
        messages = history[-20:] + [{'role': 'user', 'content': prompt}]
        try:
            answer = chat.reply(messages)
        except ValueError as error:
            print(error)
            continue
        print('Revity:', answer)
        history = messages + [{'role': 'assistant', 'content': answer}]


if __name__ == '__main__':
    main()
