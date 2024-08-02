########################################################################################################################
# Jackbox Audience Maker
# Version 2024.08.02
########################################################################################################################
# Copyright (c) 2024 Orobas
# https://www.orobas.com.au


from asyncio import run as async_run
from system.terminal import Terminal
from web.viewers import Viewers


if __name__ == "__main__":
    terminal = Terminal()
    terminal.fill("*")
    terminal.write("Jackbox Audience Maker")
    terminal.fill("*")

    room = terminal.get_string("Room Code", minimum_length=4, maximum_length=4).upper()
    fill = terminal.get_integer("Audience Number", minimum_value=1)

    viewers = async_run(Viewers().build(room, fill))
    terminal.wait()
    viewers.close()
