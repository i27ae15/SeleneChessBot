from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alpha_zero.node import GameStateNode


class StateManager:
    def __init__(self):
        self.state_dict: dict[bytes, 'GameStateNode'] = {}

    def get_state(
        self,
        board_hash: bytes,
        check_exists: bool = True,
    ) -> 'GameStateNode | False':

        if check_exists:
            if board_hash in self.state_dict:
                return self.state_dict[board_hash]
            return False

        return self.state_dict[board_hash]

    def add_state(
        self,
        game_state: 'GameStateNode',
        check_exists: bool = True,
    ) -> 'GameStateNode':

        if not check_exists:
            self.state_dict[game_state.board_hash] = game_state
            return game_state

        if game_state.board_hash not in self.state_dict:
            self.state_dict[game_state.board_hash] = game_state

    def __contains__(self, board_hash: bytes) -> bool:
        return self.get_state(board_hash)
