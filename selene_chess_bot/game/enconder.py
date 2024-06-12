from pieces import Piece
from pieces.utilites import PieceColor, RookSide

from board import Board

from game.types import FENInfo
from game.zobriest_hash import ZOBRIEST_KEYS


class GameEncoder:

    @staticmethod
    def create_fen(
        board: list[list[str]],
        active_color: PieceColor,
        castling_rights: str,
        en_passant_target: str | None,
        halfmove_clock: int,
        fullmove_number: int
    ) -> str:

        en_passant_target = en_passant_target or '-'

        color = {
            PieceColor.WHITE: 'w',
            PieceColor.BLACK: 'b'
        }

        active_color: str = color[active_color]

        fen_rows = []
        for row in board:
            empty_count = 0
            fen_row = ""
            for cell in row:
                if cell == ".":  # Empty square
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += cell
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)

        # Join all rows with '/' to form the piece placement part of the FEN
        piece_placement = "/".join(fen_rows)

        # Forming the complete FEN string
        fen = f" {piece_placement} {active_color} {castling_rights} {en_passant_target} {halfmove_clock} {fullmove_number}"
        return fen.strip()

    @staticmethod
    def parse_fen(fen: str, reverse_piece_placement: bool = True) -> FENInfo:
        parts = fen.split()
        piece_placement = parts[0]
        active_color = parts[1]
        castling_fen = parts[2]
        en_passant_target = parts[3]
        halfmove_clock = int(parts[4])
        fullmove_number = int(parts[5])

        # Create the board array
        board = []
        rows = piece_placement.split('/')
        for row in rows:
            board_row = []
            for char in row:
                if char.isdigit():
                    # Add empty squares
                    board_row.extend(['.'] * int(char))
                else:
                    # Add a piece
                    board_row.append(char)
            board.append(board_row)

        if reverse_piece_placement:
            board.reverse()

        # Convert active color
        active_color = (
            PieceColor.WHITE if active_color == 'w' else PieceColor.BLACK
        )

        # Here we assume 'en_passant_target' is a string like 'e3' or '-'
        en_passant_target = (
            None if en_passant_target == '-' else en_passant_target
        )

        # Castling rights from FEN
        castling_rights = {
            PieceColor.WHITE: {
                RookSide.KING: 'K' in castling_fen,
                RookSide.QUEEN: 'Q' in castling_fen,
            },
            PieceColor.BLACK: {
                RookSide.KING: 'k' in castling_fen,
                RookSide.QUEEN: 'q' in castling_fen,
            }
        }

        return FENInfo(
            board=board,
            active_color=active_color,
            castling_rights=castling_rights,
            en_passant_target=en_passant_target,
            halfmove_clock=halfmove_clock,
            fullmove_number=fullmove_number
        )

    @staticmethod
    def compute_game_state_hash(
        board: Board,
        en_passant_pos: str,
        castling_rights: dict,
        current_side: PieceColor,
    ):
        board_hash = 0

        # Iterate through each piece on the board and XOR its key
        for row in range(8):
            for column in range(8):
                piece = board.get_square_or_piece(row, column)
                if isinstance(piece, Piece):
                    piece: Piece
                    piece_key = ZOBRIEST_KEYS[piece.name.value[1]][piece.color][
                        (row, column)
                    ]
                    board_hash ^= piece_key

        # Include castling rights
        for side, rights in castling_rights.items():
            for right, enabled in rights.items():
                if enabled:
                    board_hash ^= ZOBRIEST_KEYS['castling'][(side, right)]

        # Include en passant possibility
        if en_passant_pos is not None:
            board_hash ^= ZOBRIEST_KEYS['en_passant'][current_side][
                int(en_passant_pos[1])
            ]

        # Include the side to move
        board_hash ^= ZOBRIEST_KEYS['side'][current_side]

        return board_hash.to_bytes(8, byteorder='big', signed=False)
    
