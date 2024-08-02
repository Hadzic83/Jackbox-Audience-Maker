########################################################################################################################
# Jackbox Audience Maker > Web > Viewers
# Version 2024.08.02
########################################################################################################################
# Copyright (c) 2024 Orobas
# https://www.orobas.com.au


from .viewer import Viewer
from asyncio import create_task as async_create, gather as async_gather


class Viewers:
    """
    Audience viewers.
    """

    # region Constructors

    def __init__(self) -> None:
        """
        Create new audience viewers.
        """

        self.__tasks = []

    # endregion

    # region Methods

    async def build(self, room: str, count: int) -> "Viewers":
        """
        Build the audience viewers.
        :param room: Room code.
        :param count: Number of audience viewers.
        :returns: This instance.
        :raises RuntimeError: If the existing viewers have not been closed.
        :raises ValueError: If the count is not a positive integer.
        """

        if self.__tasks:
            raise RuntimeError("Existing viewers have not been closed.")

        if count < 1:
            raise ValueError("Count is not a positive integer.")

        for _ in range(count):
            self.__tasks.append(async_create(Viewer().join(room)))

        await async_gather(*self.__tasks)
        return self

    def close(self) -> None:
        """
        Close all browser instances.
        """

        for task in self.__tasks:
            if task.done():
                task.result().close()
            else:
                task.cancel()

        self.__tasks.clear()

    # endregion
