# -*- coding: utf-8 -*-
"""
Lado do Servidor: Abre um TCP/IP numa port, espera por uma menssagem
de um cliente, e manda essa mensagem de volta como resposta.
Usamos aqui a biblioteca socketserver para realizar este trabalho.
Esta biblioteca fornece TCPServer, ThreadingTCPServer, ForkingTCPServer,
UDP variações destes, entre outras coisas, e redireciona cada cliente
para um 'request handler' para utilizar se método 'handle' para lidar
com o requisito do cliente.
"""
import logging
import os
import socket
import select
from handler.connection_handler import login
import config
import threading

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/server.log')

# Log, formater and file
logging.basicConfig(format='[%(asctime)s] - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=LOG_PATH,
                    level=logging.INFO)


class Worker(threading.Thread):
    def __init__(self, addr, sockfd):
        threading.Thread.__init__(self)
        self.addr = addr
        self.sockfd = sockfd

    def run(self):
        login(self.addr, self.sockfd)


if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((config.HOST, config.PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Server Started at port: {}".format(config.PORT)

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
        option = 'n'
        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                worker = Worker(addr, sockfd)
                worker.start()
