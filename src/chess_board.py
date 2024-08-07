# src/chess_board.py
import chess # https://python-chess.readthedocs.io/en/latest/index.html

class Board:
    def __init__(self):
        self.board = chess.Board() # initialize the chess board using the Board class from the python-chess library

    def move_piece(self, start_pos, end_pos):
        print(f"Moving piece from {start_pos} to {end_pos}")  # Debugging
        try:
            start_square = chess.parse_square(start_pos)
            end_square = chess.parse_square(end_pos)
        except ValueError:
            print(f"Invalid square: {start_pos} or {end_pos}")  # Debugging
            raise ValueError("Invalid square")

        move = chess.Move(start_square, end_square)
        print(f"Attempting to move: {move}")  # Debugging

        if move in self.board.legal_moves:
            self.board.push(move)
            print(f"Move {move} executed")  # Debugging
        else:
            print(f"Move {move} is illegal")  # Debugging
            raise ValueError("Invalid move")

    def is_valid_piece_move(self, start_pos, end_pos):
        try:
            start_square = chess.parse_square(start_pos)
            end_square = chess.parse_square(end_pos)
        except ValueError:
            print(f"Invalid square: {start_pos} or {end_pos}")  # Debugging
            return False

        move = chess.Move(start_square, end_square)
        is_valid = move in self.board.legal_moves
        print(f"Move validity for {start_pos} to {end_pos}: {is_valid}")  # Debugging
        return is_valid

    def is_valid_move(self, start_pos, end_pos):
        try:
            if not self.is_valid_square(start_pos) or not self.is_valid_square(end_pos):
                error_message = f"Invalid square: {start_pos} or {end_pos}"
                print(error_message)  # Debugging
                return False
            piece = self.board.board.piece_at(chess.parse_square(start_pos))
            if piece is None:
                error_message = f"No piece at start position: {start_pos}"
                print(error_message)  # Debugging
                return False
            if piece.color == self.current_turn:
                is_valid = self.board.is_valid_piece_move(start_pos, end_pos)
                print(f"Move validity for {start_pos} to {end_pos}: {is_valid}")  # Debugging
                return is_valid
            error_message = f"Piece color does not match current turn: {piece.color} vs {self.current_turn}"
            print(error_message)  # Debugging
            return False
        except Exception as e:
            print(f"Error validating move: {e}")  # Debugging
            return False

    def is_checkmate(self):
        return self.board.is_checkmate()

    def is_stalemate(self):
        return self.board.is_stalemate()

    def __str__(self):
        return self.board.unicode()

    def board_to_html(self, current_turn):
        piece_to_svg = {
            'r': 'black_rook.png',
            'n': 'black_knight.png',
            'b': 'black_bishop.png',
            'q': 'black_queen.png',
            'k': 'black_king.png',
            'p': 'black_pawn.png',
            'R': 'white_rook.png',
            'N': 'white_knight.png',
            'B': 'white_bishop.png',
            'Q': 'white_queen.png',
            'K': 'white_king.png',
            'P': 'white_pawn.png'
        }

        board_str = str(self.board)
        rows = board_str.split('\n')
        html = f"""
        <style>
            table.chess-board {{
                border-collapse: collapse;
                border: 2px solid #333;
            }}
            table.chess-board td {{
                width: 6rem;
                height: 6rem;
                text-align: center;
                vertical-align: middle;
                font-size: 2.4rem;
            }}
            table.chess-board .white {{
                background-color: #f0d9b5;
            }}
            table.chess-board .black {{
                background-color: #b58863;
            }}
        </style>

        <input type="hidden" id="current_turn" value="{current_turn}">
        <script src="/src/javascript/chess.js"></script>

        <table class="chess-board">
        """
        for i, row in enumerate(rows):
            html += '<tr>'
            for j, cell in enumerate(row.split(' ')):
                color = 'white' if (i + j) % 2 == 0 else 'black'
                cell_id = f'cell{i}{j}'
                if cell == '.':
                    html += f'<td id="{cell_id}" class="{color}" ondrop="drop(event)" ondragover="allowDrop(event)"></td>'
                else:
                    piece_svg = piece_to_svg.get(cell, '')
                    piece_id = f'piece{i}{j}'
                    html += f'<td id="{cell_id}" class="{color}" ondrop="drop(event)" ondragover="allowDrop(event)"><img id="{piece_id}" src="/static/images/chess_pieces/{piece_svg}" alt="{cell}" width="60" height="60" draggable="true" ondragstart="drag(event)"></td>'
            html += '</tr>'
        html += '</table>'
        return html