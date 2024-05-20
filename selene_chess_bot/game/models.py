import math
import uuid
import numpy as np
import json
import os
import networkx as nx

from typing import Any, Callable

from django.db import models

from pieces.utilites import PieceColor

C_VALUE = 1.414


class GameState(models.Model):

    """
    This also should act as the node in the AlphaZero tree.

    The Json for the expandable_moves and explored_moves would be in the
    following format:

    {
        'moves': ['Pe4', 'Pe5', 'Pd4', 'Pd5']
    }

    """

    # A game State can have multiple parents and multiple children
    parents = models.ManyToManyField(
        'GameState',
        related_name='children',
        blank=True
    )

    id: str = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    board_hash: bytes = models.BinaryField(unique=True)

    is_game_terminated: bool = models.BooleanField()

    white_value: float = models.FloatField()
    black_value: float = models.FloatField()

    # NOTE: The fen is necessar to be able to create a game instance
    # NOTE: Note that the current turn in the fen can vary
    fen: str = models.CharField(max_length=255, unique=True)

    player_turn: int = models.IntegerField(
        choices=PieceColor.choices
    )

    num_visits: int = models.IntegerField(default=1)
    expandable_moves: list = models.JSONField()
    explored_moves: list = models.JSONField(default=list)

    @property
    def player_turn_obj(self) -> PieceColor:
        return PieceColor(self.player_turn)

    @staticmethod
    def create_tree_representation(
        parent: 'GameState',
        visited: set = None,
        count_nodes: bool = False,
        nx_graph: nx.DiGraph = None,
        order_by: str = '-num_visits',
    ) -> nx.DiGraph:
        """
        Create the nx.Diagraph tree code representation with a DFS on the tree.
        """

        if nx_graph is None:
            nx_graph = nx.DiGraph()

        if visited is None:
            visited = set()

        # Check if the current node has already been visited
        if str(parent.board_hash) in visited:
            return nx_graph

        # Mark the current node as visited
        visited.add(str(parent.board_hash))

        if parent.children.all().count() == 0:
            return nx_graph

        children = parent.children.all().order_by(order_by)

        for child in children:
            child: GameState
            nx_graph.add_edge(str(parent.board_hash), str(child.board_hash))
            GameState.create_tree_representation(
                parent=child,
                visited=visited,
                nx_graph=nx_graph,
                order_by=order_by,
                count_nodes=count_nodes,
            )

        return nx_graph

    def add_explored_move(self, move: str) -> None:
        self.explored_moves.append(move)
        self.save()

    def add_parent(self, parent: 'GameState') -> None:
        # Postgres does not allow to add a None value to a many to many
        # field
        if parent is not None:
            self.parents.add(parent)

    def increment_visits(self):
        self.num_visits += 1
        self.save()

    def is_fully_expanded(self) -> bool:
        return len(self.expandable_moves) == self.children.all().count()

    def select(self) -> 'GameState':
        """
        Selects the child with the highest UCB1 value.
        """
        best_child = None
        best_ucb = float('-inf')

        for child in self.children.all():
            ucb = self.get_ucb(child, self.player_turn_obj)
            if ucb > best_ucb:
                best_ucb = ucb
                best_child = child

        return best_child

    def get_ucb(self, child: 'GameState', side: PieceColor) -> float:
        """
        Calculates the UCB value for the node.
        """

        values = {
            PieceColor.WHITE: self.white_value,
            PieceColor.BLACK: self.black_value
        }

        value = values[side]

        q_value = ((value / self.num_visits) + 1) / 2
        ucb = q_value + C_VALUE * math.sqrt(
            math.log(self.num_visits) / child.num_visits
        )

        return ucb

    def get_untried_move(self) -> str:
        """
        Returns a move that has not been tried yet.
        """

        move = np.random.choice(self.expandable_moves)
        self.expandable_moves.remove(move)
        self.add_explored_move(move)

        return move

    def expand(self, game_instance: Any) -> 'GameState | bool':
        """
        Expands the current node by creating a new child.
        """

        if self.is_fully_expanded():
            raise False  # No more moves to expand

        move: str = self.get_untried_move()
        move = 'Ph4'

        print(f"Taken: {move}")

        game_instance.move_piece(move)
        return game_instance.current_game_state

    def simulate(self, game: Any, delete_json: bool = False) -> float:

        """
        Game would be the pointer to the game object.
        """
        game_instance = game.parse_fen(self.fen)
        current_game_state: GameState = game_instance.current_game_state

        if self.is_game_terminated:
            return self.game_values

        while True:

            try:
                valid_moves = current_game_state.expandable_moves
                move = np.random.choice(valid_moves)

                print('-' * 50)
                print('Current move:', game_instance.current_turn)
                print('Player turn:', game_instance.player_turn)
                print('Selected move:', move)

                game_instance.move_piece(move)
                game_instance.board.print_board()
                print('-' * 50)

                if game_instance.is_game_terminated:
                    print('Game terminated successfully')
                    game_instance.print_game_state()
                    file_path = 'completed simulations.json'
                    self.save_simulation_data(file_path, game_instance)

                    return game_instance.game_values[game_instance.player_turn]

            except Exception as e:

                # Let's create a JSON file where we can store the data from
                # the game.

                print('-' * 50)
                print('error occurred')
                print(e)
                if e.__str__() == 'Invalid move at _move_piece.1':
                    print('valid moves:', valid_moves)
                    print('hash:', current_game_state.board_hash)
                print('Saving to file')
                print('-' * 50)

                file_path = 'simulation_errors.json'
                self.save_simulation_data(
                    file_path=file_path,
                    game_instance=game_instance,
                    error=e,
                    delete_json=delete_json
                )
                break

            current_game_state = game_instance.current_game_state

    def save_simulation_data(
        self,
        file_path: dict,
        game_instance: Callable,
        delete_json: bool = False,
        error: Any = None
    ) -> None:

        if delete_json:
            data = {'data': []}
        else:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r') as f:
                    data: dict = json.load(f)
            else:
                data = {
                    'data': []
                }

        white_king_in_check = game_instance.board.white_king.is_in_check
        black_king_in_check = game_instance.board.black_king.is_in_check

        data_to_append = {
            'game_state': {
                'white_king_in_check': white_king_in_check,
                'black_king_in_check': black_king_in_check,
                'is_game_terminated': game_instance.is_game_terminated,
                'is_game_drawn': game_instance.is_game_drawn,
                'moves_for_f_rule': game_instance.moves_for_f_rule,
                'fen': game_instance.current_fen,
            },
            'moves': game_instance.moves,
        }

        if error:
            data_to_append['error'] = str(error)

        values = game_instance.game_values

        data_to_append['game_values'] = {
            'white': values[PieceColor.WHITE],
            'black': values[PieceColor.BLACK]
        }
        turns = ['white', 'black']
        data_to_append['player_turn'] = turns[game_instance.player_turn.value]

        wlm = None
        try:
            wlm = game_instance.get_legal_moves(
                color=PieceColor.WHITE,
                show_in_algebraic=True,
                show_as_list=True
            )
        except Exception as e:
            print('Error getting white moves:', e)
            wlm = 'Error getting white moves: ' + str(e)

        data_to_append['wlm'] = wlm

        blm = None
        try:
            blm = game_instance.get_legal_moves(
                color=PieceColor.BLACK,
                show_in_algebraic=True,
                show_as_list=True
            )
        except Exception as e:
            print('Error getting black moves:', e)
            blm = 'Error getting black moves: ' + str(e)

        data_to_append['blm'] = blm
        data['data'].append(data_to_append)

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            print('Data saved to file')

    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)
