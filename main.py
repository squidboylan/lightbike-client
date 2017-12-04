#!/usr/bin/env python

import gui
import listener
import sys
from twisted.internet import reactor

if __name__ == "__main__":
    username = raw_input("Enter your username: ")
    #username = "caleb"

    try:
        game_size = sys.argv[1]
    except:
        game_size = "127.0.0.1"

    try:
        server_ip = sys.argv[2]
    except:
        server_ip = "127.0.0.1"

    try:
        server_port = sys.argv[3]
    except:
        server_port = 9999

    client = listener.NetClient(game_size, server_ip, server_port, username)
    reactor.listenUDP(0, client)
    reactor.run()
