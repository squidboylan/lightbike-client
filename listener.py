import gui
import threading
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class NetClient(DatagramProtocol):
    def __init__(self, server_ip, server_port, username):
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = username

    def startProtocol(self):
        self.create_game()

    def datagramReceived(self, data, (host, port)):
        split_data = data.rstrip().split()

        if split_data[0] == "AUTHACK":
            self.auth_ack(split_data)

        elif split_data[0] == "CREATE":
            self.auth()

        elif split_data[0] == "UPDATE":
            self.game_update(split_data)

        elif split_data[0] == "WINNER":
            self.game_end(split_data)

    def send_data(self, data):
        self.transport.write(data, (self.server_ip, self.server_port))

    def game_end(self, split_data):
        self.gui_obj.running = False
        self.t1.join()
        self.gui_obj.destroy()
        self.gui_obj = None
        winners = ''
        for i in split_data[1:]:
            winners = winners + i

        print 'WINNERS: ' + winners


    def update_direction(self, direction):
        self.send_data("DIRECTION " + self.token + " " + direction)

    def auth_ack(self, split_data):
        if split_data[1] == self.username:
            self.token = split_data[2]

    def auth(self):
        self.send_data("AUTH " + self.username + "\n")
        print "starting game"
        self.gui_obj = gui.Gui(self.server_ip, self.server_port, self.username, self)
        self.t1 = threading.Thread(target=self.gui_obj.run)
        self.t1.start()
        print "started game"

    def create_game(self):
        self.send_data("CREATE 2\n")

    def game_update(self, split_data):
        tmp_board = []
        for i in split_data[1:]:
            tmp_board.append(list(i))

        self.gui_obj.game_board = tmp_board
        #print tmp_board
