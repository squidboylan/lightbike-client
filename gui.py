import curses
import threading
import listener
import time
from twisted.internet import reactor

class Gui:
    def __init__(self, server_ip, server_port, username, listener):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()

        self.stdscr.keypad(1)
        self.stdscr.nodelay(1)
        curses.curs_set(0)

        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)

        self.listener = listener
        self.game_board = []
        self.pad = None
        self.running = True

    def run(self):
        while self.running:
            if len(self.game_board) != 0:
                #print self.game_board
                if not self.pad:
                    self.width = len(self.game_board[0]) * 2
                    self.height = len(self.game_board)
                    self.pad = curses.newpad(self.height, self.width)

                char = self.stdscr.getch()
                if char == curses.KEY_UP:
                    self.listener.update_direction("UP\n")
                elif char == curses.KEY_RIGHT:
                    self.listener.update_direction("RIGHT\n")
                elif char == curses.KEY_DOWN:
                    self.listener.update_direction("DOWN\n")
                elif char == curses.KEY_LEFT:
                    self.listener.update_direction("LEFT\n")
                self.draw_board()

            time.sleep(.001)


    def destroy(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        curses.curs_set(2)

    def draw_board(self):
        for i in range(len(self.game_board)):
            for j in range(len(self.game_board[i])):
                try:
                    if self.game_board[i][j] == "0":
                        self.pad.addch(i, j * 2, 32, curses.color_pair(4))
                        self.pad.addch(i, j * 2 + 1, 32, curses.color_pair(4))

                    elif self.game_board[i][j] == "1":
                        self.pad.addch(i, j * 2, 32, curses.color_pair(1))
                        self.pad.addch(i, j * 2 + 1, 32, curses.color_pair(1))

                    elif self.game_board[i][j] == "E":
                        self.pad.addch(i, j * 2, 32, curses.color_pair(2))
                        self.pad.addch(i, j * 2 + 1, 32, curses.color_pair(2))

                    elif self.game_board[i][j] == "P":
                        self.pad.addch(i, j * 2, 32, curses.color_pair(3))
                        self.pad.addch(i, j * 2 + 1, 32, curses.color_pair(3))
                except curses.error:
                    pass

        self.pad.refresh(0, 0, 1, 1, self.height, self.width)

        #self.stdscr.redrawwin()
