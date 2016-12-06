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
import config

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/server.log')

# Log, formater and file
logging.basicConfig(format='[%(asctime)s] - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=LOG_PATH,
                    level=logging.INFO)

# Tcp message server


# Function to broadcast chat messages to all connected clients
def broadcast_data(sock, message):
    # Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)


if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((config.HOST, config.PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Server Started at port: {}".format(config.PORT)

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "socket {}".format(sockfd)
                print "Client (%s, %s) connected" % addr

                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)

            # Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)

                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

        #server_socket.close()
