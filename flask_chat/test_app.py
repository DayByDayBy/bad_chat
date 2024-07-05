import unittest
from app import app

class FlaskChatTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_generate_sequence(self):
        response = self.app.post('/generate_sequence', json={
            'initial_prompt': 'Test prompt.',
            'iterations': 2
        })
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['prompts']), 3)
        self.assertEqual(len(data['responses']), 2)
        self.assertIn('Test prompt.', data['prompts'][0])

if __name__ == '__main__':
    unittest.main()
