import chess
from src.chess_board import Board

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_turn = chess.WHITE

    def play_turn(self, start_pos, end_pos):
        print(f"Playing turn: {start_pos} to {end_pos}")
        try:
            captured_piece = self.board.move_piece(start_pos, end_pos)
            if captured_piece:
                print(f"Captured piece: {captured_piece}")
            self.switch_turn()
        except ValueError as e:
            print(f"Error playing turn: {e}")
            raise

    def is_valid_move(self, start_pos, end_pos):
        try:
            if not self.board.is_valid_square(start_pos) or not self.board.is_valid_square(end_pos):
                error_message = f"Invalid square: {start_pos} or {end_pos}"
                print(error_message)
                return False
            piece = self.board.board.piece_at(chess.parse_square(start_pos))
            if piece is None:
                error_message = f"No piece at start position: {start_pos}"
                print(error_message)
                return False
            if piece.color == self.current_turn:
                is_valid = self.board.is_valid_piece_move(start_pos, end_pos)
                print(f"Move validity for {start_pos} to {end_pos}: {is_valid}")
                return is_valid
            error_message = f"Piece color does not match current turn: {piece.color} vs {self.current_turn}"
            print(error_message)
            return False
        except Exception as e:
            print(f"Error validating move: {e}")
            return False

    def switch_turn(self):
        self.current_turn = chess.BLACK if self.current_turn == chess.WHITE else chess.WHITE

    def is_game_over(self):
        try:
            return self.board.is_checkmate() or self.board.is_stalemate()
        except Exception as e:
            print(f"Error checking game over status: {e}")
            return False

    def reset(self):
        self.board = Board()
        self.current_turn = chess.WHITE