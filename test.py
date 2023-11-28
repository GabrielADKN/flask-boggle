import unittest
from app import app
from flask import session

class FlaskBoggleTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index_route(self):
        """Test index route."""
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'board', response.data)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_check_word_route(self):
        """Test check-word route."""
        with self.client:
            with self.client.session_transaction() as sess:
                sess['board'] = [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I', 'J', 'K', 'L'], ['M', 'N', 'O', 'P']]
            response = self.client.get('/check-word?word=ABC')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-word')

    def test_score_route(self):
        """Test score route."""
        with self.client:
            with self.client.session_transaction() as sess:
                sess['highscore'] = 10
                sess['nplays'] = 5
            response = self.client.post('/score', json={'score': 15})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['brokeRecord'], True)

if __name__ == '__main__':
    unittest.main()