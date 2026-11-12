import unittest
from app import app, normalize_history


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_invalid_message(self):
        response = self.client.post('/api/chat', json={'message': ''})
        self.assertEqual(response.status_code, 400)

    def test_history_filter(self):
        self.assertEqual(normalize_history([{'role': 'system', 'content': 'ignore'},
                                            {'role': 'user', 'content': ' hello '}]),
                         [{'role': 'user', 'content': 'hello'}])


if __name__ == '__main__':
    unittest.main()
