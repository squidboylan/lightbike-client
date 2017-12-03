import game
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class NetClient(DatagramProtocol):
    def __init__(self, server_ip, server_port, username, gui_obj):
        self.server_ip = server_ip
        self.server_port = server_port
        self.gui_obj = gui_obj
        self.username = username

    def startProtocol(self):
        self.transport.connect(self.server_ip, self.server_port)
        self.create_game()

    def datagramReceived(self, data, (host, port)):
        split_data = data.split()

        if split_data[0] == "AUTHACK":
            self.auth_ack(split_data)

        elif split_data[0] == "CREATE":
            self.auth()

        elif split_data[0] == "UPDATE":
            self.game_update(split_data)

    def send_data(self, data):
        self.transport.write(data)

    def auth_ack(self, split_data):
        if split_data[1] == self.username:
            self.token = split_data[2]

    def auth(self):
        self.send_data("AUTH " + self.username + "\n")

    def create_game(self):
        self.send_data("CREATE 2\n")

    def game_update(self, split_data):
        tmp_board = []
        for i in split_data[1:]:
            tmp_board.append(list(i))

        self.gui_obj.game_board = tmp_board
        #print tmp_board
