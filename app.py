from boggle import Boggle
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.secret_key = '12345'

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def index():
    """Show board."""

    board = boggle_game.make_board()
    session['board'] = board

    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)
    
    return render_template('index.html', board=board, highscore=highscore, nplays=nplays)

@app.route('/check-word')
def check_word():
    """Check if word is valid."""

    word = request.args['word']
    board = session['board']
    is_valid_word = boggle_game.check_valid_word(board, word)

    return jsonify({'result': is_valid_word})

@app.route('/score', methods=['POST'])
def score():
    """Calculate and return score."""

    score = request.json['score']
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)
    
    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)
    
    return jsonify(brokeRecord = score > highscore)

