import numpy as np

from core.printing import __print__ as pprint

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
        model_save_path: str
    ) -> None:

        for game in range(num_games):

            pprint(f"Playing game {game+1}/{num_games}...")

            game_data = []

            mcst = MCST(model=model)

            while not mcst.root.is_game_terminated:

                encoded_board = mcst.game.board.get_encoded_board()
                policy, _ = model.predict(encoded_board.reshape(1, 8, 8, 12))
                policy = policy.flatten()

                best_child_node = mcst.run(num_iterations)

                data_to_append = (encoded_board, policy, best_child_node.total_value)
                # pprint(f"Data to append: {data_to_append}")

                # save data
                game_data.append(data_to_append)

                pprint(f"Best move: {best_child_node.move}")
                mcst.game.move_piece(best_child_node.move)
                mcst.game.board.print_board(show_in_algebraic_notation=True)
                mcst.root = best_child_node  # Update this in the MCST class

            # Prepare training data
            x_train = np.array([data[0] for data in game_data])
            y_train_policy = np.array([data[1] for data in game_data])
            y_train_value = np.array([data[2] for data in game_data])

            pprint('Training model...')
            pprint(f'x_train: {x_train}', print_lines=False)
            pprint(f'y_train_policy: {y_train_policy}', print_lines=False)
            pprint(f'y_train_value: {y_train_value}', print_lines=False)

            # Train the model
            model.fit(
                x_train,
                {'policy_head': y_train_policy, 'value_head': y_train_value},
                epochs=100,
                batch_size=32
            )

        model.save(model_save_path)
        pprint('Model saved successfully!')
        return model
