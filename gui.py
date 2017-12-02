import curses
import threading
import listener
import time
from twisted.internet import reactor

class Gui:
    def __init__(self, server_ip, server_port, username):
        """
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()

        self.stdscr.keypad(1)
        self.stdscr.nodelay(1)
        curses.curs_set(0)
        """

        self.listener = listener.NetClient(server_ip, server_port, username, self)
        self.game_board = []

    def run(self):
        reactor.listenUDP(0, self.listener)
        self.t1 = threading.Thread(target=reactor.run())
        self.t1.start()

        while 1:
            if len(self.game_board) != 0:
                char = curses.getch()

            time.sleep(.001)


    def destroy(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
