# src/chess_game.py
import chess
from src.chess_board import Board

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_turn = chess.WHITE

    def play_turn(self, start_pos, end_pos, promotion_piece=chess.QUEEN):
        try:
            self.board.move_piece(start_pos, end_pos, promotion_piece)
            self.switch_turn()
        except ValueError as e:
            raise

    def is_valid_move(self, start_pos, end_pos):
        try:
            if not self.board.is_valid_square(start_pos) or not self.board.is_valid_square(end_pos):
                return False
            piece = self.board.board.piece_at(chess.parse_square(start_pos))
            if piece is None:
                return False
            if piece.color == self.current_turn:
                return self.board.is_valid_piece_move(start_pos, end_pos)
            return False
        except Exception:
            return False

    def switch_turn(self):
        self.current_turn = chess.BLACK if self.current_turn == chess.WHITE else chess.WHITE

    def is_game_over(self):
        try:
            return self.board.is_checkmate() or self.board.is_stalemate()
        except Exception:
            return False

    def reset(self):
        self.board = Board()
        self.current_turn = chess.WHITE