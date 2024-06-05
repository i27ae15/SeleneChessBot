from game.game import Game

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
