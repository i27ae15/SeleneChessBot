import json

from django.test import TestCase

from game.game import Game


class TestSimulation(TestCase):

    def setUp(self):
        self.game = Game()

    def tearDown(self) -> None:
        # self.game = Game()
        return super().tearDown()

    def test_game_from_simulation(self):
        file_path = 'simulation_errors.json'

        with open(file_path, 'r') as file:
            data: dict = json.load(file)['data']

        moves: dict[str[list]] = data[0]['moves']
        # where the number is the key and the value is the list of moves for
        # that turn

        # adding the first move that is not in the moves dictionary
        # moves['1'] = ['h4', moves['1'][0]]

        terminated = False
        for index, move in enumerate(moves):
            for move_ in moves[move]:
                print(f"{index + 1} Move: {move_}")
                if not self.game.move_piece(move_):
                    print(f"Move {move_} is not valid due to game termination")
                    terminated = True
                    break

                print('-' * 50)
                self.game.board.print_board(show_in_algebraic_notation=True)
                print('-' * 50)

            if index + 1 == 5050 or terminated:
                break

        print('-' * 50)
        print('Final board')
        color = self.game.player_turn
        self.game.board.print_board(show_in_algebraic_notation=True)

        print('-' * 50)
        print('Game State')
        self.game.print_game_state()

        expandable_moves = self.game.current_game_state.expandable_moves
        print('-' * 50)
        print(f'getting legal moves for {color}')
        m = self.game.get_legal_moves(
            color=color,
            show_in_algebraic=True,
            show_as_list=True
        )
        print(f'Legal moves for {color}')
        print(sorted(m))
        print('-' * 50)
        print('expandable moves')
        print(sorted(expandable_moves))

        MOVE = 'gxf3'

        print('-' * 50)
        print('move', MOVE)
        print('move in expable_move', MOVE in expandable_moves)
        print('move in legal move', MOVE in m)
        print('-' * 50)

        print('makig move')
        self.game.move_piece(MOVE)
        print('-' * 50)
        self.game.board.print_board(show_in_algebraic_notation=True)
        print(self.game.current_game_state.expandable_moves)
