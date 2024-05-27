from selene_chess_bot.alpha_zero.node import GameStateNode
from pieces.utilites import PieceColor


class StateManager:
    def __init__(self):
        self.state_dict: dict[bytes, GameStateNode] = {}

    def get_state(
        self,
        board_hash: bytes,
        player_turn: PieceColor
    ) -> GameStateNode:
        if board_hash in self.state_dict:
            return self.state_dict[board_hash]
        else:
            new_state = GameStateNode(board_hash, player_turn)
            self.state_dict[board_hash] = new_state
            return new_state

    def add_state(
        self,
        board_hash: bytes,
        player_turn: PieceColor
    ) -> GameStateNode:
        if board_hash not in self.state_dict:
            new_state = GameStateNode(board_hash, player_turn)
            self.state_dict[board_hash] = new_state
        return self.state_dict[board_hash]
