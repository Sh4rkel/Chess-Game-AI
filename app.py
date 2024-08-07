from flask import Flask, request, jsonify, send_from_directory # https://flask.palletsprojects.com/en/3.0.x/quickstart/#static-files
import chess # https://python-chess.readthedocs.io/en/latest/index.html
from src.chess_game import ChessGame
"""

Simple Flask server to host the chess game,
I want to remake it in the future when I finish to implement
a reinforcement learning model to play against the AI.

"""
app = Flask(__name__)
game = ChessGame()

@app.route('/')
def index():
    try:
        board_html = game.board.board_to_html('white' if game.current_turn == chess.WHITE else 'black')
        return f'<h1>Welcome to the Chess Game!</h1>{board_html}'
    except Exception as e:
        print(f"Error rendering index: {e}")  # Debugging (useless until now)
        return "Internal Server Error", 500

@app.route('/move', methods=['POST'])
def move():
    try:
        data = request.get_json()
        start_pos = data.get('start_pos')
        end_pos = data.get('end_pos')
        print(f"Received move request: {start_pos} to {end_pos}")  # Debugging (useless until now)
        if game.is_valid_move(start_pos, end_pos):
            game.play_turn(start_pos, end_pos)
            return jsonify({'status': 'success', 'board': game.board.board_to_html('white' if game.current_turn == chess.WHITE else 'black')})
        else:
            error_message = f"Invalid move from {start_pos} to {end_pos}"
            print(error_message)  # Debugging (useless until now)
            return jsonify({'status': 'error', 'message': error_message})
    except Exception as e:
        print(f"Error processing move: {e}")  # Debugging (useless until now)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    try:
        return jsonify({'game_over': game.is_game_over(), 'current_turn': 'white' if game.current_turn == chess.WHITE else 'black'})
    except Exception as e:
        print(f"Error fetching status: {e}")  # Debugging (useless until now)
        return "Internal Server Error", 500

@app.route('/src/javascript/<path:filename>')
def serve_js(filename):
    return send_from_directory('src/javascript', filename)

if __name__ == '__main__':
    app.run()