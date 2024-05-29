from game.game import Game

from alpha_zero.mcst import MCST
from alpha_zero.node import GameStateNode
from alpha_zero.state_manager import StateManager


class AlphaZero:

    def __init__(
        self,
        depth_of_search: int,
    ) -> None:

        self.depth_of_search = depth_of_search

    def play_game(self):
        state_manager = StateManager()
        game: Game = Game()

        best_move: GameStateNode = GameStateNode.create_game_state(
            move=None,
            game=game,
            state_manager=state_manager,
        )

        while not game.is_game_terminated:

            mcst = MCST(
                root=best_move,
                state_manager=state_manager,
            )

            best_move = mcst.run(
                iterations=self.depth_of_search,
            )

            print(f'Best move: {best_move.move}')
            return
            game.move_piece(best_move.move)

            print('-' * 50)
            game.board.print_board(show_in_algebraic_notation=True)
            print('-' * 50)

        return game
