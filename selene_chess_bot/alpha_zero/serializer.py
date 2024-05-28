import pickle

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alpha_zero.node import GameStateNode


class Checkpoint:

    def __init__(self) -> None:

        self.root = None
        self.filename: str = 'checkpoint.pkl'

        self._is_initialized = False

    @staticmethod
    def save_checkpoint(
        root: 'GameStateNode',
        filename: str = 'checkpoint.pkl'
    ) -> bool:

        with open(filename, 'wb') as f:
            pickle.dump(root, f)

        return True

    def load_checkpoint(self, filename: str = None) -> 'GameStateNode':
        if self._is_initialized:
            return self.root

        if not filename:
            filename = self.filename

        with open(filename, 'rb') as f:
            root = pickle.load(f)

        self.root = root
        self._is_initialized = True

        return root
