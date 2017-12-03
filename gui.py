import curses
import threading
import listener
import time
from twisted.internet import reactor

class Gui:
    def __init__(self, server_ip, server_port, username):
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

        self.listener = listener.NetClient(server_ip, server_port, username, self)
        self.game_board = []
        self.pad = None

    def run(self):
        reactor.listenUDP(0, self.listener)
        self.t1 = threading.Thread(target=reactor.run())
        self.t1.start()

        while 1:
            if len(self.game_board) != 0:
                if not self.pad:
                    self.width = len(self.game_board[0])
                    self.height = len(self.game_board)
                    self.pad = curses.newpad(self.height, self.width)

                char = self.stdscr.getch()
                if char == curses.KEY_UP:
                    self.listener.send_data("DIRECTION UP\n")
                elif char == curses.KEY_RIGHT:
                    self.listener.send_data("DIRECTION RIGHT\n")
                elif char == curses.KEY_DOWN:
                    self.listener.send_data("DIRECTION DOWN\n")
                elif char == curses.KEY_LEFT:
                    self.listener.send_data("DIRECTION LEFT\n")

                self.draw_board()

            time.sleep(.001)


    def destroy(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def draw_board(self):
        for i in range(len(self.game_board)):
            for j in range(len(self.game_board[i])):
                try:
                    if self.game_board[i][j] == "0":
                        self.pad.addch(i, j, 32, curses.color_pair(4))

                    elif self.game_board[i][j] == "1":
                        self.pad.addch(i, j, 32, curses.color_pair(1))

                    elif self.game_board[i][j] == "E":
                        self.pad.addch(i, j, 32, curses.color_pair(2))

                    elif self.game_board[i][j] == "P":
                        self.pad.addch(i, j, 32, curses.color_pair(3))
                except curses.error:
                    pass

                self.pad.refresh(0, 0, 1, 1, self.height, self.width)

        #self.stdscr.redrawwin()
