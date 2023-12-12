import json
import random

WHITE_TO_MOVE = 0
BLACK_TO_MOVE = 1
ALL_LONDON_LINES = (0, 1, 2, 3, 4, 5, 6, 7, 8)


class ChessGame:

    def __init__(
        self,
        file_path: str,
        lines_number: list[int] | tuple[int] = ALL_LONDON_LINES,
        move_as: int = WHITE_TO_MOVE
    ):
        self.file_path: str = file_path
        self.lines: str = lines_number
        self.move_as: int = move_as  # 0 = white, 1 = black
        self.chess_moves_dict: dict = self.convert_json_to_dict()

        self.moves_being_played: list[dict] = []
        self.current_main_line: dict = {}
        self.current_chessly_line: int = 0
        self.lines_played: int = 0
        self.lines_to_play: int = 0

    def __str__(self):
        return f"{self.title}: {self.lines}"

    def convert_json_to_dict(self):
        with open(self.file_path, 'r') as json_file:
            data = json.load(json_file)
        return data

    def get_lines(self) -> list[dict]:
        """

            Build a list that looks like this

            [
                {
                    'title': 'str ...',
                    'lines': [int ....]
                } ...
            ]

        """

        lines: list[dict] = []

        for line in self.lines:

            chess_line: dict = self.chess_moves_dict[line]

            dict_line: dict = {
                'index': line,
                'title': chess_line['title'],
                'lines': [line for line in range(len(chess_line['lines']))]
            }
            lines.append(dict_line)

            # calculate the number of lines to play
            self.lines_to_play += len(chess_line['lines'])

        return lines

    def get_chessly_line(self) -> dict:
        return self.chess_moves_dict[
            self.current_main_line['index']
        ]['lines'][self.current_chessly_line]

    def get_exercises_line(self, available_main_lines: list[dict]) -> dict:
        # get_random_main_line
        self.current_main_line = random.choice(available_main_lines)

        # get random chessly line
        self.current_chessly_line = random.choice(
            self.current_main_line['lines']
        )

        # strip that line from the list
        self.current_main_line['lines'].remove(self.current_chessly_line)

        # check if the lines are empty and remove them from the list
        if len(self.current_main_line['lines']) == 0:
            available_main_lines.remove(self.current_main_line)

        return self.get_chessly_line()

    def show_moves(self):

        """
            Show the moves that are being played

            in this way

                1. d4 d5
                2. Bf4 e6
        """

        for index, move in enumerate(self.moves_being_played):
            print(f'{index + 1}. {move["white"]} {move["black"]}')

    def show_lines_to_play(self):
        print(f'Lines played: {self.lines_played + 1}/{self.lines_to_play}')

    def check_input(self, input: str) -> bool:

        if input == 'q':
            print('Bye!')
            exit()

        if input == 'r':
            self.start_game()
            return False

        if input == 'showmoves':
            self.show_moves()
            return True

        if input == 'showlines':
            self.show_lines_to_play()

        return False

    def start_game(self):

        available_main_lines = self.get_lines()

        # start playing

        while available_main_lines:
            # get the line
            chosen_line_to_play = self.get_exercises_line(available_main_lines)

            print('-----------------------------------')
            print(f'Line title: {self.current_main_line["title"]}')
            print(f'Chessly line number: {self.current_chessly_line + 1}')
            self.show_lines_to_play()

            # play the line

            self.current_move: int = 1
            self.moves_being_played = []

            for move in chosen_line_to_play['moves']:
                correct_move: str = str()
                move_to_do: str = input('Your move: ')

                while self.check_input(move_to_do):
                    move_to_do = input('Your move: ')

                # TODO: add long castle as LC and short castle as SC

                if self.move_as == WHITE_TO_MOVE:

                    # check if the move is correct
                    correct_move = move_to_do

                    if move_to_do != move['white']:
                        print('Wrong!')
                        print(f'Correct move: {move["white"]}')
                        correct_move = move['white']

                    print(f'black: {move["black"]}')

                    move_played = {
                        'white': correct_move,
                        'black': move['black'],
                    }
                    self.moves_being_played.append(move_played)

                self.current_move += 1

            self.lines_played += 1


json_file_path = 'files/london_system_chessly_lines.json'
chess_game = ChessGame(json_file_path, [7])
chess_game.start_game()
