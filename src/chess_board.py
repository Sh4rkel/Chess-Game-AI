import chess

class Board:
    def __init__(self):
        self.board = chess.Board()
        self.captured_pieces = []

    def move_piece(self, start_pos, end_pos, promotion=None):
        try:
            start_square = chess.parse_square(start_pos)
            end_square = chess.parse_square(end_pos)
        except ValueError:
            raise ValueError("Invalid square")

        if promotion:
            promotion_piece = chess.Piece.from_symbol(promotion).piece_type
        else:
            promotion_piece = None

        move = chess.Move(start_square, end_square, promotion=promotion_piece)
        if move in self.board.legal_moves:
            if self.board.is_capture(move):
                captured_piece = self.board.piece_at(end_square)
                self.captured_pieces.append(captured_piece.symbol())
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
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .game-container {{
                display: flex;
                margin-top: 20px;
            }}
            .chess-board {{
                border-collapse: collapse;
                border: 2px solid #333;
            }}
            .chess-board td {{
                width: 6rem;
                height: 6rem;
                text-align: center;
                vertical-align: middle;
                font-size: 2.4rem;
            }}
            .chess-board .white {{
                background-color: #f0d9b5;
            }}
            .chess-board .black {{
                background-color: #b58863;
            }}
            .move-list {{
                margin-left: 20px;
                width: 200px;
            }}
            .move-list h3 {{
                margin-top: 0;
            }}
            .move-list ul {{
                list-style-type: none;
                padding: 0;
            }}
            .move-list li {{
                background-color: #eee;
                margin: 5px 0;
                padding: 5px;
                border-radius: 5px;
            }}
            .timers {{
                display: flex;
                justify-content: space-between;
                width: 100%;
            }}
            .timers span {{
                font-size: 1.2rem;
                margin: 0 10px;
            }}
        </style>
        <div class="container">
            <h1>Welcome to the Chess Game!</h1>
            <div class="timers">
                <span>White Timer: <span id="white-timer">5:00</span></span>
                <span>Black Timer: <span id="black-timer">5:00</span></span>
            </div>
            <input type="hidden" id="current_turn" value="{current_turn}">
            <script src="/src/javascript/chess.js"></script>
            <div class="game-container">
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
        html += """
                <div class="move-list">
                    <h3>Move List</h3>
                    <ul id="move-list"></ul>
                </div>
            </div>
        </div>
        """
        return html

    def get_captured_pieces(self):
        return self.captured_pieces