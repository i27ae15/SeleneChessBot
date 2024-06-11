from typing import Any

from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CustomPrint(metaclass=SingletonMeta):
    """
    CustomPrint class for printing text with debug lines and colors based on
    the type of the argument. Implements Singleton design pattern.
    """

    def __init__(
        self,
        debug: bool = True,
        line_color: str = Fore.WHITE,
        string_color: str = Fore.GREEN,
        int_color: str = Fore.BLUE,
        dict_list_color: str = Fore.LIGHTYELLOW_EX
    ) -> None:
        """
        Initializes the CustomPrint class.

        :param debug: Enables or disables debug lines. Default is True.
        :param line_color: Color for the debug lines. Default is Fore.WHITE.
        :param string_color: Color for string arguments. Default is Fore.GREEN.
        :param int_color: Color for integer arguments. Default is Fore.BLUE.
        :param dict_list_color: Color for dictionary and list arguments.
            Default is Fore.LIGHTYELLOW_EX.
        """
        self.debug: bool = debug
        self.line_color: str = line_color
        self.string_color: str = string_color
        self.int_color: str = int_color
        self.dict_list_color: str = dict_list_color

    def __call__(
        self,
        *args: Any,
        print_lines: bool = True,
        line_length: int = 50,
        **kwargs: Any
    ) -> None:
        """
        Prints the arguments with appropriate colors based on their types,
        surrounded by debug lines if enabled.

        :param print_lines: Whether to print the debug lines. Default is True.
        :param line_length: Length of the debug lines. Default is 50.
        """
        if self.debug and print_lines:
            print(self.line_color + '-' * line_length + Style.RESET_ALL)

        colored_args = []
        for arg in args:

            if isinstance(arg, str):
                colored_args.append(
                    self.string_color + str(arg) + Style.RESET_ALL
                )

            elif isinstance(arg, int):
                colored_args.append(
                    self.int_color + str(arg) + Style.RESET_ALL
                )

            elif isinstance(arg, (dict, list)):
                colored_args.append(
                    self.dict_list_color + str(arg) + Style.RESET_ALL
                )

            else:
                colored_args.append(str(arg))

        print(*colored_args, **kwargs)

        if self.debug and print_lines:
            print(self.line_color + '-' * line_length + Style.RESET_ALL)

    def set_debug(self, debug: bool) -> None:
        """
        Sets the debug mode.

        :param debug: Enables or disables debug lines.
        """
        self.debug = debug

    def set_line_color(self, line_color: str) -> None:
        """
        Sets the color for the debug lines.

        :param line_color: Color for the debug lines, from colorama.Fore.
        """
        self.line_color = line_color

    def set_string_color(self, string_color: str) -> None:
        """
        Sets the color for string arguments.

        :param string_color: Color for string arguments, from colorama.Fore.
        """
        self.string_color = string_color

    def set_int_color(self, int_color: str) -> None:
        """
        Sets the color for integer arguments.

        :param int_color: Color for integer arguments, from colorama.Fore.
        """
        self.int_color = int_color

    def set_dict_list_color(self, dict_list_color: str) -> None:
        """
        Sets the color for dictionary and list arguments.

        :param dict_list_color: Color for dictionary and list arguments,
        from colorama.Fore.
        """
        self.dict_list_color = dict_list_color


__print__ = CustomPrint()
