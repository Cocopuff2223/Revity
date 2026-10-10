"""Single-user browser chat. Bind to loopback only; no public hosting support."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from .chat import Chat, DEFAULT_MODEL, ROOT


def handler_for(chat):
    class Handler(BaseHTTPRequestHandler):
        def send(self, status, body, kind='application/json'):
            self.send_response(status)
            self.send_header('Content-Type', kind)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == '/':
                self.send(200, (ROOT / 'web/index.html').read_bytes(), 'text/html; charset=utf-8')
            elif self.path == '/health':
                self.send(200, b'{"ready":true,"model":"Qwen3-0.6B","fine_tuned":false}')
            else:
                self.send(404, b'{"error":"Not found"}')

        def do_POST(self):
            if self.path != '/chat':
                self.send(404, b'{"error":"Not found"}')
                return
            # JSON and same-origin checks prevent other browser sites from posting prompts.
            expected_origin = f'http://{self.headers.get("Host", "")}'
            if self.headers.get('Origin') not in (None, expected_origin) or self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
                self.send(403, b'{"error":"Only same-origin JSON requests are accepted"}')
                return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 64000:
                    raise ValueError('Request must contain 1–64000 bytes.')
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError('Request must be an object.')
                answer = chat.reply(data.get('messages'), data.get('max_new_tokens', 256))
                self.send(200, json.dumps({'reply': answer}).encode())
            except (ValueError, UnicodeDecodeError) as error:
                self.send(400, json.dumps({'error': str(error)}).encode())
            except Exception:
                self.send(500, b'{"error":"Generation failed. Check server logs."}')
                import traceback
                traceback.print_exc()
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, default=DEFAULT_MODEL)
    parser.add_argument('--port', type=int, default=7860)
    args = parser.parse_args()
    chat = Chat(args.model)
    server = HTTPServer(('127.0.0.1', args.port), handler_for(chat))
    print(f'Revity is ready on local port {args.port}. Ctrl+C to stop.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
