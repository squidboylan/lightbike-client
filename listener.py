import game
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Listener(DatagramProtocol):
    def __init__(self, game_obj):
        self.game_obj = game_obj

    def datagramReceived(self, data, (host, port)):
