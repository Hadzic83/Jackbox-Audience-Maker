########################################################################################################################
# Jackbox Audience Maker
# Version 2024.08.03
########################################################################################################################
# Copyright (c) 2024 Orobas
# https://www.orobas.com.au


from asyncio import run as async_run
from sys import argv as system_arguments
from system.terminal import Terminal
from web.viewers import Viewers


__CODE_LENGTH = 4

if __name__ == "__main__":
    terminal = Terminal()
    terminal.fill("*")
    terminal.write("Jackbox Audience Maker")
    terminal.fill("*")

    if len(system_arguments) == 3:
        try:
            room = system_arguments[1]
            fill = int(system_arguments[2])

            if len(room) != __CODE_LENGTH or fill < 1:
                room = None
                fill = None

        except ValueError:
            room = None
            fill = None
    else:
        room = None
        fill = None

    if not room or not fill:
        room = terminal.get_string(
            "Room Code",
            minimum_length=__CODE_LENGTH,
            maximum_length=__CODE_LENGTH
        ).upper()
        fill = terminal.get_integer("Audience Number", minimum_value=1)
    else:
        terminal.write(f"Room Code: {room}")
        terminal.write(f"Audience Number: {fill}")

    viewers = async_run(Viewers().build(room, fill))
    terminal.wait()
    viewers.close()
