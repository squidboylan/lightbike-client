import game
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class NetClient(DatagramProtocol):
    def __init__(self, server_ip, server_port, username, gui_obj):
        self.server_ip = server_ip
        self.server_port = server_port
        self.gui_obj = gui_obj
        self.username = username


    def connectionMade(self):
        self.auth()

    def datagramReceived(self, data, (host, port)):
        split_data = data.split()
        if split_data[0] == "AUTHACK":
            self.auth_ack(split_data)

    def send_data(self, data):
        self.transport.write(data, (self.server_ip, self.server_port))

    def auth_ack(self, split_data):
        if split_data[1] == self.username:
            self.token = split_data[2]

    def auth(self):
        self.transport.write("AUTH " + self.username + "\n", (self.server_ip, self.server_port))
