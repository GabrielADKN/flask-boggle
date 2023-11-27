from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Boggle Game', response.data)

    def test_start_game(self):
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'board', session)

    def test_guess_word(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['board'] = [['A', 'B', 'C', 'D', 'E'],
                                 ['F', 'G', 'H', 'I', 'J'],
                                 ['K', 'L', 'M', 'N', 'O'],
                                 ['P', 'Q', 'R', 'S', 'T'],
                                 ['U', 'V', 'W', 'X', 'Y']]
            response = self.client.post('/guess', data={'word': 'DOG'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'result', session)
            self.assertIn(b'word', session['result'])
            self.assertIn(b'score', session['result'])

    def test_invalid_word(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['board'] = [['A', 'B', 'C', 'D', 'E'],
                                 ['F', 'G', 'H', 'I', 'J'],
                                 ['K', 'L', 'M', 'N', 'O'],
                                 ['P', 'Q', 'R', 'S', 'T'],
                                 ['U', 'V', 'W', 'X', 'Y']]
            response = self.client.post('/guess', data={'word': 'INVALID'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'result', session)
            self.assertIn(b'word', session['result'])
            self.assertIn(b'score', session['result'])
            self.assertEqual(session['result']['score'], 0)

if __name__ == '__main__':
    unittest.main()