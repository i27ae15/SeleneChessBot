import traceback

import numpy as np

from core.printing import __print__ as pprint
from core.saver import FileSaver

from game import Game

from alpha_zero.mcst import MCST
from alpha_zero.node import GameStateNode
from alpha_zero.state_manager import StateManager


class AlphaZero:

    def __init__(
        self,
        depth_of_search: int,
        mcst_exploration_weight: float = 1.414,
    ) -> None:

        self.root: GameStateNode = None
        self.depth_of_search: int = depth_of_search
        self.mcst_exploration_weight: float = mcst_exploration_weight
        self.games_played = 0
        self.games_played_list: list[Game] = []

    def play_game(self) -> GameStateNode:
        state_manager = StateManager()
        game: Game = Game()

        best_move: GameStateNode = GameStateNode.create_game_state(
            move=None,
            game=game,
            state_manager=state_manager,
        )
        self.root = best_move

        while not game.is_game_terminated:

            mcst = MCST(
                root=best_move,
                state_manager=state_manager,
                exploration_weight=self.mcst_exploration_weight,
            )

            best_move = mcst.run(
                iterations=self.depth_of_search,
            )

            print('-' * 50)
            print(f'Best move: {best_move}')
            game.move_piece(best_move)
            game.board.print_board(show_in_algebraic_notation=True)
            print('-' * 50)

            if game.is_game_terminated:
                print('Game terminated.')
                break

            best_move = GameStateNode.create_game_state(
                move=None,
                game=game,
                state_manager=state_manager,
            )

        self.games_played += 1
        self.games_played_list.append(game)

        game.print_game_state()
        return self.root

    def self_play(
        self,
        model,
        num_games: int,
        num_iterations: int,
        train_model: bool = True,
        model_save_path: str = None
    ) -> None:

        for game in range(num_games):

            pprint(f"Playing game {game+1}/{num_games}...")

            game_data: list[tuple] = []
            mcst: MCST = MCST(model=model)

            while not mcst.root.is_game_terminated:
                try:
                    best_child_node = mcst.run(num_iterations)
                    data_to_append = self.get_state_data(
                        model=model,
                        game=mcst.game,
                        best_node=best_child_node
                    )

                    game_data.append(data_to_append)

                    # Moving the piece after exploring multiple states
                    # on the MCST
                    mcst.update_game_state(best_child_node)

                    pprint('best_move:', best_child_node.move)
                    mcst.game.board.print_board(
                        show_in_algebraic_notation=True
                    )

                except Exception as e:
                    self.manage_error(mcst, e)
                    return

            # Train the model
            if train_model:
                self.train_model(model=model, raw_game_data=game_data)
            # Save the model
            if model_save_path:
                self.save_model(model=model, model_save_path=model_save_path)

        return model

    def manage_error(self, mcst: MCST, e: Exception) -> None:

        # TODO: Convert this to a logging system class
        error_message = ''.join(
            traceback.format_exception(None, e, e.__traceback__)
        )

        data_to_save = mcst.game.get_game_state(json_format=True)
        data_to_save['game_moves'] = mcst.game.moves
        data_to_save['error_message'] = error_message.split('\n')

        file_name = FileSaver.json_saver(
            data_to_save=mcst.game.get_game_state(json_format=True)
        )

        pprint(
            f'Error: {error_message}, saved at {file_name}',
            print_lines=False
        )

    def get_state_data(
        self,
        game: Game,
        model: object,
        best_node: GameStateNode
    ) -> tuple:

        encoded_board: np.ndarray = game.board.get_encoded_board()
        policy, _ = model.predict(encoded_board.reshape(1, 8, 8, 12))
        policy = policy.flatten()

        data = (encoded_board, policy, best_node.total_value)

        return data

    def train_model(self, model: object, raw_game_data: list):

        """
        X_train: Encoded board in a numpy array of shape (8, 8, 12)


        """

        # Prepare training data
        x_train = np.array([data[0] for data in raw_game_data])
        y_train_policy = np.array([data[1] for data in raw_game_data])
        y_train_value = np.array([data[2] for data in raw_game_data])

        pprint('Training model...')
        pprint(f'x_train: {x_train}', print_lines=False)
        pprint(f'y_train_policy: {y_train_policy}', print_lines=False)
        pprint(f'y_train_value: {y_train_value}', print_lines=False)

        model.fit(
            x_train,
            {'policy_head': y_train_policy, 'value_head': y_train_value},
            epochs=100,
            batch_size=32
        )

        pprint('Model trained successfully!')

    def save_model(self, model: object, model_save_path: str) -> None:

        # check if model_save_path has a .keras extension
        if not model_save_path.endswith('.keras'):
            model_save_path += '.keras'

        model.save(model_save_path)
        pprint('Model saved successfully!')
