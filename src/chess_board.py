import chess

class Board:
    def __init__(self):
        self.board = chess.Board()

    def move_piece(self, start_pos, end_pos, promotion=None):
        try:
            start_square = chess.parse_square(start_pos)
            end_square = chess.parse_square(end_pos)
        except ValueError:
            raise ValueError("Invalid square")

        move = chess.Move(start_square, end_square, promotion=chess.Piece.from_symbol(promotion).piece_type if promotion else None)
        if move in self.board.legal_moves:
            self.board.push(move)
        else:
            raise ValueError("Invalid move")

    def is_valid_piece_move(self, start_pos, end_pos):
        try:
            start_square = chess.parse_square(start_pos)
            end_square = chess.parse_square(end_pos)
        except ValueError:
            return False

        move = chess.Move(start_square, end_square)
        return move in self.board.legal_moves

    def is_valid_square(self, square):
        return square in chess.SQUARE_NAMES

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