from flask import Flask, request, jsonify, send_from_directory
import chess
from src.chess_game import ChessGame
from src.data_collection import collect_game_data
from src.ai_chess import load_model, ai_move

app = Flask(__name__)
game = ChessGame()
model = load_model()
@app.route('/')
def index():
    try:
        board_html = game.board.board_to_html('white' if game.current_turn == chess.WHITE else 'black')
        return f'<h1>Welcome to the Chess Game!</h1>{board_html}'
    except Exception as e:
        print(f"Error rendering index: {e}")
        return "Internal Server Error", 500

@app.route('/move', methods=['POST'])
def move():
    try:
        data = request.get_json()
        start_pos = data.get('start_pos')
        end_pos = data.get('end_pos')
        promotion = data.get('promotion')

        if game.is_valid_move(start_pos, end_pos):
            game.play_turn(start_pos, end_pos, promotion)
            board_html = game.board.board_to_html('white' if game.current_turn == chess.WHITE else 'black')
            move_notation = f"{start_pos} to {end_pos}"
            return jsonify({'status': 'success', 'board': board_html, 'move': move_notation})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid move'})
    except Exception as e:
        print(f"Error processing move: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/ai_move', methods=['POST'])
def ai_move_route():
    try:
        if game.current_turn == chess.BLACK:  # Assuming AI plays as black
            if ai_move(game, model):
                board_html = game.board.board_to_html('white' if game.current_turn == chess.WHITE else 'black')
                return jsonify({'status': 'success', 'board': board_html})
            else:
                return jsonify({'status': 'error', 'message': 'AI move failed'})
        else:
            return jsonify({'status': 'error', 'message': 'Not AI\'s turn'})
    except Exception as e:
        print(f"Error processing AI move: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    try:
        return jsonify({'game_over': game.is_game_over(), 'current_turn': 'white' if game.current_turn == chess.WHITE else 'black'})
    except Exception as e:
        print(f"Error fetching status: {e}")
        return "Internal Server Error", 500

@app.route('/captured_pieces', methods=['GET'])
def captured_pieces():
    try:
        pieces = game.get_captured_pieces()
        return jsonify({'captured_pieces': pieces})
    except Exception as e:
        print(f"Error fetching captured pieces: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/reset_timers', methods=['POST'])
def reset_timers():
    try:
        game.reset_timers()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error resetting timers: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    try:
        game.reset()
        board_html = game.board.board_to_html('white')
        return jsonify({'status': 'success', 'board': board_html})
    except Exception as e:
        print(f"Error resetting game: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/src/javascript/<path:filename>')
def serve_js(filename):
    return send_from_directory('src/javascript', filename)

@app.route('/game_data', methods=['GET'])
def game_data():
    try:
        data = collect_game_data(game)
        return jsonify(data)
    except Exception as e:
        print(f"Error collecting game data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run()