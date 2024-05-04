from pieces.utilites import PieceColor


class StateCommand:
    def execute(self, context):
        raise NotImplementedError


class PrintBoardCommand(StateCommand):
    def execute(self, context):
        context.game.board.print_board()


class PrintBoardAlgebraicCommand(StateCommand):
    def execute(self, context):
        context.game.board.print_board(show_in_algebraic_notation=True)


class PrintStateCommand(StateCommand):
    def execute(self, context):
        context.game.print_game_state()


class SquaresAttackedByBlackCommand(StateCommand):
    def execute(self, context):
        context.game.board.print_attacked_squares(
            perspective=PieceColor.BLACK,
            show_in_algebraic_notation=True
        )


class SquaresAttackedByWhiteCommand(StateCommand):
    def execute(self, context):
        context.game.board.print_attacked_squares(
            perspective=PieceColor.WHITE,
            show_in_algebraic_notation=True
        )


class GetPiecesAttackingBlackKingCommand(StateCommand):
    def execute(self, context):
        print(context.game.board.black_king.get_pieces_attacking_me())


class GetPiecesAttackingWhiteKingCommand(StateCommand):
    def execute(self, context):
        print(context.game.board.white_king.get_pieces_attacking_me())


class GetWhiteLegalMovesCommand(StateCommand):
    def execute(self, context):
        print(context.game.board.get_legal_moves(PieceColor.WHITE, True))


class GetBlackLegalMovesCommand(StateCommand):
    def execute(self, context):
        print(context.game.board.get_legal_moves(PieceColor.BLACK, True))


class GetMovesDoneCommand(StateCommand):
    def execute(self, context):
        print(context.game.moves)


class GetPiecesOnBoardCommand(StateCommand):
    def execute(self, context):
        print(context.game.board.pieces_on_board)


class GetBoardStatesCommand(StateCommand):
    def execute(self, context):
        print(context.game.board_states)


class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.commands = {
            'board': PrintBoardCommand(),
            'state': PrintStateCommand(),
            'boardl': PrintBoardAlgebraicCommand(),
            'sab': SquaresAttackedByBlackCommand(),
            'saw': SquaresAttackedByWhiteCommand(),
            'pabk': GetPiecesAttackingBlackKingCommand(),
            'pawk': GetPiecesAttackingWhiteKingCommand(),
            'wlm': GetWhiteLegalMovesCommand(),
            'blm': GetBlackLegalMovesCommand(),
            'moves': GetMovesDoneCommand(),
            'pieces': GetPiecesOnBoardCommand(),
            'bst': GetBoardStatesCommand(),
        }

    def execute_command(self, command_key) -> bool:

        """

        This function will execute the command given by the user.

        if the command is not found, it will return False. Otherwise, it will.
        returns True

        """

        if command_key == 'help':
            self.help_command()
            return True

        if command_key in self.commands:
            self.commands[command_key].execute(self)
            return True

        return False

    def help_command(self):
        for key in self.commands:
            print(key)


def debug_before_move_decorator(func):
    def wrapper(self, move, color, *args, **kwargs):
        if self.debug:

            if self._wait_for_move:
                if self.game.current_turn == self._wait_for_move:
                    self._wait_for_move = False
                else:
                    return func(self, move, color, *args, **kwargs)

            debugger = GameStateManager(self.game)
            print('-' * 50)
            while True:
                text = input('->:').strip()
                if not text or text == 'next':
                    print(color.name, move)
                    break

                splitted_text = text.split(' ')
                if splitted_text[0] == 'gtm':
                    if len(splitted_text) > 1:
                        self._wait_for_move = int(splitted_text[1])
                    else:
                        self._wait_for_move = int(input('move:'))
                    print('going to move', self._wait_for_move)
                    break

                debugger.execute_command(text)

        return func(self, move, color, *args, **kwargs)
    return wrapper


def debug_at_end_of_moves(cls=None, game=None, force=False):

    if force or cls.debug:
        game = game or cls.game

        debugger = GameStateManager(game)
        print('-' * 50)
        while True:
            text = input('->:').strip()
            if not text:
                break

            debugger.execute_command(text)


def control_state_manager(game) -> str:
    game_state_manager = GameStateManager(game)
    while True:
        text = input('->:').strip()
        comand_not_found = game_state_manager.execute_command(text)

        if not comand_not_found:
            break

    return text
