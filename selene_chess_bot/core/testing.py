import sys


class BColors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def print_success(text: str = None, show_line: bool = True):
    if not text:
        print(f'{BColors.OKGREEN}OK{BColors.ENDC}')
    else:
        print(f'{BColors.OKGREEN}{text}{BColors.ENDC}')

    if show_line:
        print('-'*70)


def print_starting(text=None):
    if not text:
        frame = sys._getframe(1)
        func_name = frame.f_code.co_name
        print(f'{BColors.OKBLUE}Testing: {func_name}{BColors.ENDC}')
    else:
        print(f'{BColors.OKBLUE}{text}{BColors.ENDC}')


def print_warning(text):
    print(f'{BColors.WARNING}{text}{BColors.ENDC}')


def print_error(text):
    print(f'{BColors.FAIL}{text}{BColors.ENDC}')
