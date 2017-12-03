#!/usr/bin/env python

import gui
import sys

if __name__ == "__main__":
    username = raw_input("Enter your username: ")
    #username = "caleb"
    try:
        server_ip = sys.argv[1]
    except:
        server_ip = "127.0.0.1"

    try:
        server_port = sys.argv[2]
    except:
        server_port = 9999

    try:
        client = gui.Gui(server_ip, server_port, username)
        client.run()
    finally:
        client.destroy()
