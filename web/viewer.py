########################################################################################################################
# Jackbox Audience Maker > Web > Viewer
# Version 2024.08.03
########################################################################################################################
# Copyright (c) 2024 Orobas
# https://www.orobas.com.au


from os import remove as os_remove
from os.path import dirname as path_directory, expanduser as path_expand, join as path_join, realpath as path_real
from platform import system as platform_system
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome as ChromeDriver, ChromeOptions, ChromeService
from selenium.webdriver.common.by import By as FindBy
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from uuid import uuid4


class Viewer:
    """
    Audience viewer.
    """

    # region Globals

    __options = None
    """
    Chrome driver options.
    """

    __service = None
    """
    Chrome driver service.
    """

    # endregion

    # region Constructors

    def __init__(self) -> None:
        """
        Create a new audience viewer.
        """

        self.__browser = None

    # endregion

    # region Properties

    @property
    def __agent__(self) -> str:
        """
        Gets the user agent for the current operating system.
        :return: The user agent for the current operating system.
        :raises RuntimeError: If the current operating system is not supported.
        """

        if self.os_linux:
            return Viewer.__OPTION_AGENT_LINUX

        if self.os_macintosh:
            return Viewer.__OPTION_AGENT_MACINTOSH

        if self.os_windows:
            return Viewer.__OPTION_AGENT_WINDOWS

        raise RuntimeError("Operating system is not supported.")

    @property
    def __bin__(self) -> str:
        """
        Gets the path to the bin directory.
        :return: The path to the bin directory.
        """

        current_directory = path_expand(path_directory(path_real(__file__)))
        return path_real(path_join(current_directory, "..", "bin"))

    @property
    def __browser__(self) -> ChromeDriver:
        """
        Gets the browser instance.
        :return: The browser instance.
        """

        if not self.__browser:
            self.__browser = ChromeDriver(self.__options__, self.__service__)
            self.__browser.set_window_size(720, 576)

        return self.__browser

    @property
    def __options__(self) -> ChromeOptions:
        """
        Gets the browser options.
        :return: The browser options.
        """

        if not Viewer.__options:
            Viewer.__options = ChromeOptions()
            Viewer.__options.binary_location = self.path_browser
            Viewer.__options.add_argument(self.__agent__)

            if Viewer.__RUN_HEADLESS:
                Viewer.__options.add_argument(Viewer.__OPTION_HEADLESS)

        return Viewer.__options

    @property
    def os_linux(self) -> bool:
        """
        Determines whether the current operating system is Linux.
        :return: True if the current operating system is Linux; otherwise, false.
        """

        return platform_system() == Viewer.__OS_LINUX

    @property
    def os_macintosh(self) -> bool:
        """
        Determines whether the current operating system is Macintosh.
        :return: True if the current operating system is Macintosh; otherwise, false.
        """

        return platform_system() == Viewer.__OS_MACINTOSH

    @property
    def os_windows(self) -> bool:
        """
        Determines whether the current operating system is Windows.
        :return: True if the current operating system is Windows; otherwise, false.
        """

        return platform_system() == Viewer.__OS_WINDOWS

    # noinspection DuplicatedCode
    @property
    def path_browser(self) -> str:
        """
        Gets the path to the relevant browser for the current operating system.
        :return: The path to the relevant browser for the current operating system.
        :raises RuntimeError: If the current operating system is not supported.
        """

        if self.os_linux:
            return path_join(self.__bin__, Viewer.__BROWSER_LINUX_DIRECTORY, Viewer.__BROWSER_LINUX_FILE)

        if self.os_macintosh:
            return path_join(self.__bin__, Viewer.__BROWSER_MACINTOSH_DIRECTORY, Viewer.__BROWSER_MACINTOSH_FILE)

        if self.os_windows:
            return path_join(self.__bin__, Viewer.__BROWSER_WINDOWS_DIRECTORY, Viewer.__BROWSER_WINDOWS_FILE)

        raise RuntimeError("Operating system is not supported.")

    # noinspection DuplicatedCode
    @property
    def path_driver(self) -> str:
        """
        Gets the path to the relevant driver for the current operating system.
        :return: The path to the relevant driver for the current operating system.
        :raises RuntimeError: If the current operating system is not supported.
        """

        if self.os_linux:
            return path_join(self.__bin__, Viewer.__DRIVER_LINUX_DIRECTORY, Viewer.__DRIVER_LINUX_FILE)

        if self.os_macintosh:
            return path_join(self.__bin__, Viewer.__DRIVER_MACINTOSH_DIRECTORY, Viewer.__DRIVER_MACINTOSH_FILE)

        if self.os_windows:
            return path_join(self.__bin__, Viewer.__DRIVER_WINDOWS_DIRECTORY, Viewer.__DRIVER_WINDOWS_FILE)

        raise RuntimeError("Operating system is not supported.")

    @property
    def __service__(self) -> ChromeService:
        """
        Gets the browser service.
        :return: The browser service.
        """

        if not Viewer.__service:
            Viewer.__service = ChromeService(executable_path=self.path_driver)
            Viewer.__service.start()

        return Viewer.__service

    # endregion

    # region Methods

    def close(self) -> None:
        """
        Close the browser instance.
        """

        self.__browser__.close()

    async def join(self, room: str) -> "Viewer":
        """
        Join a game.
        :param room: Room code.
        :return: This instance.
        :throws RuntimeError: If the game could not be joined.
        """

        self.__browser__.get(Viewer.__JOIN_URL)

        name = uuid4().hex
        file = path_join(self.__bin__, f"{name}{Viewer.__JOIN_EXTENSION}")
        wait = WebDriverWait(self.__browser__, Viewer.__JOIN_WAIT)

        try:
            wait.until(expect.element_to_be_clickable((FindBy.ID, Viewer.__JOIN_ROOM))).send_keys(room)
            wait.until(expect.element_to_be_clickable((FindBy.ID, Viewer.__JOIN_NAME))).send_keys(name)
        except TimeoutException:
            raise RuntimeError("Game could not be joined.")

        attempts = Viewer.__JOIN_ATTEMPTS

        while attempts > 0:
            if Viewer.__RUN_DEBUGGING:
                self.__browser__.save_screenshot(file)

            try:
                wait.until(expect.element_to_be_clickable((FindBy.ID, Viewer.__JOIN_BUTTON))).click()

                if Viewer.__RUN_DEBUGGING:
                    os_remove(file)

                return self
            except TimeoutException:
                attempts -= 1

        raise RuntimeError("Game could not be joined.")

    # endregion

    # region Constants

    __BROWSER_LINUX_DIRECTORY = "chrome-linux64"
    """
    Browser directory for the Linux operating system.
    """

    __BROWSER_LINUX_FILE = "chrome"
    """
    Browser file for the Linux operating system.
    """

    __BROWSER_MACINTOSH_DIRECTORY = "chrome-mac-x64"
    """
    Browser directory for the Macintosh operating system.
    """

    __BROWSER_MACINTOSH_FILE = "Google Chrome for Testing.app"
    """
    Browser file for the Macintosh operating system.
    """

    __BROWSER_WINDOWS_DIRECTORY = "chrome-win64"
    """
    Browser directory for the Windows operating system.
    """

    __BROWSER_WINDOWS_FILE = "chrome.exe"
    """
    Browser file for the Windows operating system.
    """

    __DRIVER_LINUX_DIRECTORY = "chromedriver-linux64"
    """
    Driver directory for the Linux operating system.
    """

    __DRIVER_LINUX_FILE = "chromedriver"
    """
    Driver file for the Linux operating system.
    """

    __DRIVER_MACINTOSH_DIRECTORY = "chromedriver-mac-x64"
    """
    Driver directory for the Macintosh operating system.
    """

    __DRIVER_MACINTOSH_FILE = "chromedriver"
    """
    Driver file for the Macintosh operating system.
    """

    __DRIVER_WINDOWS_DIRECTORY = "chromedriver-win64"
    """
    Driver directory for the Windows operating system.
    """

    __DRIVER_WINDOWS_FILE = "chromedriver.exe"
    """
    Driver file for the Windows operating system.
    """

    __JOIN_ATTEMPTS = 3
    """
    The number of times to attempt to join a game before failing.
    """

    __JOIN_BUTTON = "button-join"
    """
    Identifier of the HTML element that is clicked to join the game.
    """

    __JOIN_EXTENSION = ".png"
    """
    File extension for screenshots.
    """

    __JOIN_NAME = "username"
    """
    Identifier of the HTML element that accepts the user's name.
    """

    __JOIN_ROOM = "roomcode"
    """
    Identifier of the HTML element that accepts the room code.
    """

    __JOIN_URL = "https://jackbox.tv"
    """
    URL to the webpage for joining a game.
    """

    __JOIN_WAIT = 10.0
    """
    Amount of time, in seconds, to wait before clicking the button to join the game.
    """

    __OPTION_AGENT_LINUX = "--user-agent=" +\
                           "Mozilla/5.0 (X11; Linux x86_64) " +\
                           "AppleWebKit/537.36 (KHTML, like Gecko) " +\
                           "Chrome/123.0.0.0 Safari/537.36"
    """
    User agent for Linux operating systems.
    """

    __OPTION_AGENT_MACINTOSH = "--user-agent=" +\
                               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " +\
                               "AppleWebKit/537.36 (KHTML, like Gecko) " +\
                               "Chrome/123.0.0.0 Safari/537.36"
    """
    User agent for Macintosh operating systems.
    """

    __OPTION_AGENT_WINDOWS = "--user-agent=" +\
                             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +\
                             "AppleWebKit/537.36 (KHTML, like Gecko) " +\
                             "Chrome/123.0.0.0 Safari/537.36"
    """
    User agent for Windows operating systems.
    """

    __OPTION_HEADLESS = "--headless=new"
    """
    Hides the browser's interface.
    """

    __OS_LINUX = "Linux"
    """
    Linux operating system identifier.
    """

    __OS_MACINTOSH = "Darwin"
    """
    Macintosh operating system identifier.
    """

    __OS_WINDOWS = "Windows"
    """
    Windows operating system identifier.
    """

    __RUN_DEBUGGING = False
    """
    True to save a screenshot if the browser if the game cannot be loaded.
    """

    __RUN_HEADLESS = True
    """
    True to run in headless mode; otherwise, false.
    """

    # endregion
