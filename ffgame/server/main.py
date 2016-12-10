# -*- coding: utf-8 -*-
"""
 This is a simple socket server to development of the Full Fight Game (FFG), just receive datagram via socket and start
 a worker to handle this socket request, this server accept simultaneous connections, to play just telnet address-server
 port 5000, feel free to contribute to this adventure =)
"""
import logging
import os
import socket
import select
from handler.connection_handler import login
import config
import threading
from model.user import Char

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/server.log')

# Log, formater and file
logging.basicConfig(format='[%(asctime)s] - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=LOG_PATH,
                    level=logging.INFO)


class Worker(threading.Thread):
    """
    Just run callback method
    """
    def __init__(self, _addr, _sockfd, _callback):
        threading.Thread.__init__(self)
        self.addr = _addr
        self.sockfd = _sockfd
        self.callback = _callback

    def run(self):
        self.callback(self.addr, self.sockfd)


if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((config.HOST, config.PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    logging.info("Server Started bind:{} at port:{}".format(config.HOST, config.PORT))
    print("Server Started bind:{} port:{}".format(config.HOST, config.PORT))

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)

                try:
                    worker = Worker(addr, sockfd, login)
                    worker.start()
                except Exception:
                    pass
            else:
                try:
                    data = sock.recv(1024)
                except Exception as e:
                    print("Execption DATA", e)
                    data = 0

                if data:
                    print("DATA", data)  # Would append device to "devices" dictionary
                else:
                    sockfd.close()
                    CONNECTION_LIST.remove(sockfd)
                    try:
                        player = Char.find_player_by_conn(sockfd)
                        Char.close(player, sockfd)
                    except IndexError:
                        pass

                    logging.info("Client Close connection by quit addr: {} socket:{}".format(addr, sockfd))
                    print("Closed {}".format(sockfd))
