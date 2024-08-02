########################################################################################################################
# Jackbox Audience Maker > System > Terminal
# Version 2024.08.02
########################################################################################################################
# Copyright (c) 2024 Orobas
# https://www.orobas.com.au


from os import get_terminal_size
from typing import Any, Tuple


class Terminal:
    """
    Terminal helper.
    """

    # region Properties

    @property
    def height(self) -> int:
        """
        Gets the number of characters that can be displayed vertically in the terminal.
        :return: The number of characters that can be displayed vertically in the terminal.
        """

        try:
            return get_terminal_size().lines
        except OSError:
            return Terminal.__DEFAULT_HEIGHT

    @property
    def width(self) -> int:
        """
        Gets the number of characters that can be displayed horizontally in the terminal.
        :return: The number of characters that can be displayed horizontally in the terminal.
        """

        try:
            return get_terminal_size().columns
        except OSError:
            return Terminal.__DEFAULT_WIDTH

    # endregion

    # region Methods

    def clear(self) -> None:
        """
        Clear the terminal with blank lines.
        """

        for _ in range(self.height):
            print()

    def fill(self, content: str) -> None:
        """
        Fill a row with the specified content.
        :param content: Content with which to fill the row.
        :raises ValueError: If the content is blank.
        """

        if not content:
            raise ValueError("The content is blank.")

        value = ""

        while len(value) < self.width:
            value += content

        print(value[:self.width])

    def get_choice(self, prompt: str, *args: Tuple[str, str], **kwargs: Any) -> str:
        """
        Gets input from the terminal and returns it as a choice identifier.
        :param prompt: Input prompt.
        :param args: Positional arguments of identifier and description pairs.
        :param kwargs: Keyword arguments.
        :keyword default: str, Default identifier if none entered, defaults to none.
        :return: The response from the user as a choice identifier.
        :raises ValueError: If there are no choices provided.
        """

        if len(args) == 0:
            raise ValueError("No choices provided.")

        options = [(option[0].strip().lower(), option[1].strip()) for option in args]
        default = kwargs.get("default", None)
        longest = 0

        if isinstance(default, str):
            default = default.strip().upper()

        for option in options:
            longest = max(longest, len(option[0]))

        while True:
            print(f"{prompt} (choose one):")

            for option in options:
                if option[0].upper() == default:
                    print(f"  {''.ljust(longest - len(default))}[{default}] {option[1]}")
                else:
                    print(f"  {''.ljust(longest - len(option[0]))}[{option[0]}] {option[1]}")

            choice = self.__input__("Choice", False).lower()

            if any(choice == option[0] for option in options):
                return choice

            if not choice and isinstance(default, str):
                return default

    def get_integer(self, prompt: str, **kwargs: Any) -> int:
        """
        Gets input from the terminal and returns it as an integer.
        :param prompt: Input prompt.
        :param kwargs: Keyword arguments.
        :keyword minimum_value: int, Minimum value of the input, defaults to no limit.
        :keyword maximum_value: int, Maximum value of the input, defaults to no limit.
        :return: The response from the user as an integer.
        :raises ValueError: If the minimum value is greater than the maximum value.
        """

        minimum_value = kwargs.get("minimum_value", None)
        maximum_value = kwargs.get("maximum_value", None)

        if minimum_value is not None and maximum_value is not None and minimum_value > maximum_value:
            raise ValueError("Minimum value is greater than the maximum value.")

        if minimum_value is not None and maximum_value is not None:
            prompt += f" (between {minimum_value}-{maximum_value})"
        elif minimum_value is not None:
            prompt += f" (at least {minimum_value})"
        elif maximum_value is not None:
            prompt += f" (at most {maximum_value})"

        while True:
            response = self.__input__(prompt, True)

            try:
                value = int(response)

                if isinstance(minimum_value, int) and value < minimum_value:
                    continue

                if isinstance(maximum_value, int) and value > maximum_value:
                    continue

                return value
            except ValueError:
                continue

    def get_string(self, prompt: str, **kwargs: Any) -> str:
        """
        Gets input from the terminal and returns it as a string.
        :param prompt: Input prompt.
        :param kwargs: Keyword arguments.
        :keyword minimum_length: int, Minimum length of the input, defaults to no limit.
        :keyword maximum_length: int, Maximum length of the input, defaults to no limit.
        :return: The response from the user as a string.
        :raises ValueError: If the minimum length is greater than the maximum length.
        """

        minimum_length = max(kwargs.get("minimum_length", 0), 0)
        maximum_length = max(kwargs.get("maximum_length", 0), 0)

        if minimum_length > maximum_length:
            raise ValueError("Minimum length is greater than the maximum length.")

        if minimum_length > 0 and maximum_length > 0:
            if minimum_length == maximum_length:
                prompt += f" ({minimum_length} character{'s' if minimum_length > 1 else ''})"
            else:
                prompt += f" ({minimum_length}-{maximum_length} characters)"
        elif minimum_length > 0:
            prompt += f"(at least {minimum_length} character{'s' if minimum_length > 1 else ''})"
        elif maximum_length > 0:
            prompt += f"(at most {maximum_length} character{'s' if maximum_length > 1 else ''})"

        while True:
            response = self.__input__(prompt, minimum_length > 0)

            if 0 < minimum_length > len(response):
                continue

            if 0 < maximum_length < len(response):
                continue

            return response

    # noinspection PyMethodMayBeStatic
    def __input__(self, prompt: str, required: bool = True) -> str:
        """
        Gets input from the terminal.
        :param prompt: Input prompt.
        :param required: True if a response is required; otherwise, false.
        :return: The response from the user.
        """

        while True:
            response = input(f"{prompt}: ").strip()

            if response or not required:
                return response

    # noinspection PyMethodMayBeStatic
    def wait(self, message: str = "Press Enter to continue...") -> None:
        """
        Wait for the user to press enter.
        :param message: Message to be displayed.
        """

        input(message)

    def write(self, content: str, overflow: bool = True) -> bool:
        """
        Write text to the terminal.
        :param content: Content to be written.
        :param overflow: True to allow the text to overflow to a new line; otherwise, false.
        :return: True if the text was displayed in full; otherwise, false.
        """

        if overflow or len(content) < self.width:
            print(content)
            return True

        print(content[:self.width])
        return False

    # endregion

    # region Constants

    __DEFAULT_HEIGHT = 24
    """
    Default height of the terminal.
    """

    __DEFAULT_WIDTH = 80
    """
    Default width of the terminal.
    """

    # endregion
