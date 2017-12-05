import gui
import threading
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class NetClient(DatagramProtocol):
    # Initialize our class data
    def __init__(self, game_size, server_ip, server_port, username):
        self.game_size = game_size
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = username

    # Create the game when we conncet to the port
    def startProtocol(self):
        self.create_game()

    # When we receive data, split it and hand it off to the correct function to
    # do what is appropriate with the data
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

    # Send data to the server
    def send_data(self, data):
        self.transport.write(data, (self.server_ip, self.server_port))

    # After winners have been declared, end the game and show the user who won
    def game_end(self, split_data):
        self.gui_obj.running = False
        self.t1.join()
        self.gui_obj.destroy()
        self.gui_obj = None
        winners = ''
        for i in split_data[1:]:
            winners = winners + i + " "

        print 'WINNERS: ' + winners


    # Update the direction the user is facing by telling the server
    def update_direction(self, direction):
        self.send_data("DIRECTION " + self.token + " " + direction)

    # When we receive an AUTHACK, keep track of our token
    def auth_ack(self, split_data):
        if split_data[1] == self.username:
            self.token = split_data[2]

    # Send AUTH data and create our game and start it in a separate thread
    def auth(self):
        self.send_data("AUTH " + self.username + "\n")
        print "starting game"
        self.gui_obj = gui.Gui(self.server_ip, self.server_port, self.username, self)
        self.t1 = threading.Thread(target=self.gui_obj.run)
        self.t1.start()
        print "started game"

    # Create a new game of size self.game_size
    def create_game(self):
        self.send_data("CREATE " + self.game_size + "\n")

    # When we get an update from the server, update the game
    def game_update(self, split_data):
        tmp_board = []
        for i in split_data[1:]:
            tmp_board.append(list(i))

        self.gui_obj.game_board = tmp_board
        self.gui_obj.time_since_update = 0
