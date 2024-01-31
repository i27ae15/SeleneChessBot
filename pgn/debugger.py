from pieces.utilites import PieceColor


class DebugCommand:
    def execute(self, context):
        raise NotImplementedError


class PrintBoardCommand(DebugCommand):
    def execute(self, context):
        context.game.board.print_board()


class PrintBoardAlgebraicCommand(DebugCommand):
    def execute(self, context):
        context.game.board.print_board(show_in_algebraic_notation=True)


class PrintStateCommand(DebugCommand):
    def execute(self, context):
        context.game.print_game_state()


class SquaresAttackedByBlackCommand(DebugCommand):
    def execute(self, context):
        context.game.board.print_attacked_squares(
            perspective=PieceColor.BLACK,
            show_in_algebraic_notation=True
        )


class SquaresAttackedByWhiteCommand(DebugCommand):
    def execute(self, context):
        context.game.board.print_attacked_squares(
            perspective=PieceColor.WHITE,
            show_in_algebraic_notation=True
        )


class GetPiecesAttackingBlackKingCommand(DebugCommand):
    def execute(self, context):
        print(context.game.board.black_king.get_pieces_attacking_me())


class GetPiecesAttackingWhiteKingCommand(DebugCommand):
    def execute(self, context):
        print(context.game.board.white_king.get_pieces_attacking_me())


class GetWhiteLegalMovesCommand(DebugCommand):
    def execute(self, context):
        print(context.game.board.get_legal_moves(PieceColor.WHITE, True))


class GetBlackLegalMovesCommand(DebugCommand):
    def execute(self, context):
        print(context.game.board.get_legal_moves(PieceColor.BLACK, True))


class Debugger:
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
            # Map other commands
        }

    def execute_command(self, command_key):

        if command_key == 'help':
            self.help_command()
            return

        if command_key in self.commands:
            self.commands[command_key].execute(self)

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

            debugger = Debugger(self.game)
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


def debug_at_end_of_moves(cls):

    if cls.debug:

        debugger = Debugger(cls.game)
        print('-' * 50)
        while True:
            text = input('->:').strip()
            if not text:
                break

            debugger.execute_command(text)
