from src.chess_game import ChessGame

def collect_game_data(game: ChessGame):
    data = {
        'board': game.board.board_to_fen(),
        'current_turn': 'white' if game.current_turn == chess.WHITE else 'black',
        'white_timer': game.white_timer,
        'black_timer': game.black_timer,
        'captured_pieces': game.get_captured_pieces(),
        'move_history': game.board.move_stack
    }
    return data