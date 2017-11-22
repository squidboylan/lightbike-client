#!/usr/bin/env python

import game

if __name__ == "__main__":
    try:
        client = game.Game()
    except:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        raise
