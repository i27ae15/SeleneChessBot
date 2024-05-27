import math
import json
import os
import numpy as np

from typing import Any, TYPE_CHECKING

from pieces.utilites import PieceColor


if TYPE_CHECKING:
    from game.game import Game

C_VALUE = 1.414


class GameStateNode:

    def __init__(
        self,
        game: 'Game',
        exploration_weight: float = 1.0
    ) -> None:

        self.game: 'Game' = game

        self.parents: set['GameStateNode'] = set()
        self.children: dict[bytes, 'GameStateNode'] = {}  # Using a dict to map moves to child nodes
        self.board_hash: bytes = game.current_board_hash
        self.is_game_terminated: bool = False

        self.white_value: float = 0.0
        self.black_value: float = 0.0
        self.fen: str = game.current_fen

        self.player_turn: PieceColor = game.player_turn
        self.num_visits: int = 0
        self.total_value: float = 0.0  # Cumulative value from simulations

        self.expandable_moves: set['GameStateNode'] = set()  # List of moves that can be expanded
        self.explored_moves: set['GameStateNode'] = set()  # List of moves that have been explored

        self.policy: dict[bytes, float] = {}  # Prior probabilities from NN for each move
        self.exploration_weight: float = exploration_weight

    @property
    def game_values(self) -> dict[PieceColor, float]:
        return {
            PieceColor.WHITE: self.white_value,
            PieceColor.BLACK: self.black_value
        }

    @property
    def is_fully_expanded(self) -> bool:
        return len(self.expandable_moves) == 0

    def add_explored_move(self, game_state: 'GameStateNode') -> None:
        self.explored_moves.add(game_state)

    def add_parent(self, parent: 'GameStateNode') -> None:
        if parent is None:
            return
        self.parents.add(parent)

    def increment_visits(self):
        self.num_visits += 1

    def select(self) -> 'GameStateNode':
        """
        Selects the child with the highest UCB value.
        """
        best_child = None
        best_ucb = float('-inf')

        for child in self.children:
            ucb = self.get_ucb(child, self.player_turn)
            if ucb > best_ucb:
                best_ucb = ucb
                best_child = child

        return best_child

    def get_ucb(self, child: 'GameStateNode', side: PieceColor) -> float:
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

    def get_random_move(self) -> str:
        """
        Returns a random move from the list of explored moves.
        """
        return np.random.choice(self.expandable_moves)

    def expand(self, game_instance: 'Game') -> 'GameStateNode | bool':
        """
        Expands the current node by creating a new child.
        """

        # if self.is_fully_expanded():
        #     raise False  # No more moves to expand

        move: str = self.get_random_move()
        game_instance.move_piece(move)
        return game_instance.current_game_state, move

    def simulate(
        self,
        game: 'Game',
        delete_json: bool = False,
        print_helpers: bool = False,
        first_move: str = None,
        save_data: bool = True
    ) -> float:

        """
        Game would be the pointer to the game object.
        """
        game_instance = game.parse_fen(self.fen)
        current_game_state: GameStateNode = game_instance.current_game_state

        if self.is_game_terminated:
            return self.game_values

        while True:

            try:
                valid_moves = current_game_state.expandable_moves
                move = np.random.choice(valid_moves)

                if print_helpers:
                    print('-' * 50)
                    print('Current move:', game_instance.current_turn)
                    print('Player turn:', game_instance.player_turn)
                    print('Selected move:', move)

                game_instance.move_piece(move)

                if print_helpers:
                    game_instance.board.print_board()
                    print('-' * 50)

                if game_instance.is_game_terminated:
                    if print_helpers:
                        print('Game terminated successfully')
                        game_instance.print_game_state()
                    file_path = 'completed_simulations.json'

                    if save_data:
                        self.save_simulation_data(
                            file_path,
                            game_instance,
                            first_move=first_move,
                        )

                    return game_instance.game_values

            except Exception as e:

                # Let's create a JSON file where we can store the data from
                # the game.

                print('-' * 50)
                print('error occurred')
                print('last move:', move)
                print(e)
                print('valid moves:', valid_moves)
                print('hash:', current_game_state.board_hash)
                print('Saving to file')
                print('-' * 50)

                file_path = 'simulation_errors.json'
                self.save_simulation_data(
                    file_path=file_path,
                    game_instance=game_instance,
                    error=e,
                    delete_json=delete_json,
                    print_helpers=print_helpers,
                    last_move=move,
                    first_move=first_move
                )
                raise Exception('Error occurred during simulation')

            current_game_state = game_instance.current_game_state

    def save_simulation_data(
        self,
        file_path: dict,
        game_instance: 'Game',
        delete_json: bool = False,
        error: Any = None,
        print_helpers: bool = False,
        last_move: str = None,
        first_move: str = None
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

        white_king_in_check = 'No data'
        black_king_in_check = 'No data'

        try:
            white_king_in_check = game_instance.board.white_king.is_in_check
        except Exception as e:
            print('Error getting white king in check:', e)

        try:
            black_king_in_check = game_instance.board.black_king.is_in_check
        except Exception as e:
            print('Error getting black king in check:', e)

        black_king_in_check = game_instance.board.black_king.is_in_check

        moves = game_instance.moves
        moves[1] = [first_move, moves[1][0]]

        data_to_append = {
            'game_state': {
                'white_king_in_check': white_king_in_check,
                'black_king_in_check': black_king_in_check,
                'is_game_terminated': game_instance.is_game_terminated,
                'is_game_drawn': game_instance.is_game_drawn,
                'moves_for_f_rule': game_instance.moves_for_f_rule,
                'fen': game_instance.current_fen,
            },
            'moves': moves,
            'last_move': last_move if last_move else 'No move selected'
        }

        if error:
            data_to_append['error'] = str(error)

        values = game_instance.game_values

        if values[PieceColor.WHITE] == 'inf':
            values[PieceColor.WHITE] = 999999999

        if values[PieceColor.BLACK] == 'inf':
            values[PieceColor.BLACK] = 999999999

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
            if print_helpers:
                print('Data saved to file')
