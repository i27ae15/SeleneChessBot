import dill

from collections import deque

# import pickle

from alpha_zero.node import GameStateNode


class Checkpoint:

    def __init__(self) -> None:

        self.root = None
        self.filename: str = 'checkpoint.pkl'

        self._is_initialized = False

    @staticmethod
    def flatten_tree(
        root: 'GameStateNode',
    ) -> list:

        node_list = []
        visited = set()
        queue = deque([root])

        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)

            node_data = {
                'fen': node.fen,
                'move': node.move,
                'result': node.result,
                'board_hash': node.board_hash,
                'player_turn': node.player_turn,
                'is_game_terminated': node.is_game_terminated,
                'expandable_moves': node.expandable_moves,
                'parents': [p.board_hash for p in node.parents],  # Store references to parent nodes
                'children': [c.board_hash for c in node.children.values()]  # Store references to child nodes
            }
            node_list.append(node_data)
            for child in node.children.values():
                if child not in visited:
                    queue.append(child)

        return node_list

    @classmethod
    def save_checkpoint(
        cls,
        root: 'GameStateNode',
        flatten: bool = False,
        filename: str = 'checkpoint.pkl'
    ) -> bool:

        if flatten:
            root = cls.flatten_tree(root)

        with open(filename, 'wb') as f:
            dill.dump(root, f)

        return True

    def load_checkpoint(self, filename: str = None) -> 'GameStateNode':
        if self._is_initialized:
            return self.root

        if not filename:
            filename = self.filename

        with open(filename, 'rb') as f:
            node_list = dill.load(f)

        node_map = {node_data['board_hash']: GameStateNode(**node_data) for node_data in node_list}

        for node_data in node_list:
            node = node_map[node_data['board_hash']]
            node.parents = {node_map[phash] for phash in node_data['parents']}
            node.children = {chash: node_map[chash] for chash in node_data['children']}

        self.root = node_map[node_list[0]['board_hash']]
        self._is_initialized = True

        return self.root

    def no_flat_load_checkpoint(self, filename: str = None) -> 'GameStateNode':
        if self._is_initialized:
            return self.root

        if not filename:
            filename = self.filename

        with open(filename, 'rb') as f:
            root = dill.load(f)

        self.root = root
        self._is_initialized = True

        return root
