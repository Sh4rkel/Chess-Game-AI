import chess
from src.chess_board import Board

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_turn = chess.WHITE
        self.white_timer = 300
        self.black_timer = 300

    def play_turn(self, start_pos, end_pos, promotion=None):
        try:
            self.board.move_piece(start_pos, end_pos, promotion)
            self.switch_turn()
            self.reset_timers()
        except ValueError as e:
            raise ValueError(str(e))

    def is_valid_move(self, start_pos, end_pos):
        try:
            if not self.board.is_valid_square(start_pos) or not self.board.is_valid_square(end_pos):
                return False
            piece = self.board.board.piece_at(chess.parse_square(start_pos))
            if piece is None or piece.color != self.current_turn:
                return False
            return self.board.is_valid_piece_move(start_pos, end_pos)
        except Exception as e:
            return False

    def switch_turn(self):
        self.current_turn = chess.BLACK if self.current_turn == chess.WHITE else chess.WHITE

    def is_game_over(self):
        try:
            return self.board.is_checkmate() or self.board.is_stalemate()
        except Exception as e:
            return False

    def reset(self):
        self.board = Board()
        self.current_turn = chess.WHITE
        self.reset_timers()

    def reset_timers(self):
        self.white_timer = 300
        self.black_timer = 300

    def get_captured_pieces(self):
        return self.board.get_captured_pieces()