import http.client
import json
import threading
import unittest
from http.server import HTTPServer
from revity.chat import Chat
from revity.server import handler_for


class FakeChat:
    def reply(self, messages, max_new_tokens=256):
        if not messages:
            raise ValueError('Messages required')
        return 'test reply'


class ChatValidationTests(unittest.TestCase):
    def test_rejects_bad_history_before_inference(self):
        chat = object.__new__(Chat)
        for messages in (None, [], [{'role': 'system', 'content': 'x'}], [{'role': 'user', 'content': ''}], [{'role': 'user', 'content': 'x'*8001}]):
            with self.assertRaises(ValueError):
                chat.reply(messages)


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.server = HTTPServer(('127.0.0.1', 0), handler_for(FakeChat()))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.client = http.client.HTTPConnection('127.0.0.1', self.server.server_port)

    def tearDown(self):
        self.client.close()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def post(self, payload, origin=None):
        headers = {'Content-Type': 'application/json'}
        if origin:
            headers['Origin'] = origin
        self.client.request('POST', '/chat', json.dumps(payload), headers)
        response = self.client.getresponse()
        return response.status, json.loads(response.read())

    def test_serves_page(self):
        self.client.request('GET', '/')
        response = self.client.getresponse()
        self.assertEqual(response.status, 200)
        self.assertIn(b'Powered by Qwen3-0.6B', response.read())

    def test_chat_route(self):
        status, body = self.post({'messages': [{'role': 'user', 'content': 'hello'}]})
        self.assertEqual(status, 200)
        self.assertEqual(body['reply'], 'test reply')

    def test_rejects_invalid_request(self):
        self.assertEqual(self.post({'messages': []})[0], 400)
        self.assertEqual(self.post([])[0], 400)

    def test_rejects_cross_origin(self):
        self.assertEqual(self.post({'messages': []}, 'https://example.com')[0], 403)


if __name__ == '__main__':
    unittest.main()
