# -*- coding: utf-8 -*-
"""
 Class to manage bussines requests
"""
import logging
from model.user import User

RECV_BUFFER = 4096


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def login(addr, sockfd):
    option = 'n'
    # Handle the case in which there is a new connection recieved through server_socket
    logging.info("Client {} Connected".format(addr))
    cavera(sockfd)
    sockfd.send(Bcolors.OKBLUE)
    logo(sockfd)
    sockfd.send(Bcolors.ENDC)
    while option == 'n':
        sockfd.send("Digite seu Email e pressione Enter ou Crt-c para Sair\n")
        email = sockfd.recv(RECV_BUFFER)[:-2]
        sockfd.send(Bcolors.FAIL+"E-mail: {}\nConfirma? s/n? ".format(email)+Bcolors.ENDC)
        op = sockfd.recv(RECV_BUFFER)[:-2]
        if op == 's':
            option = op
    User.open(email, sockfd)
    online_users(sockfd)
    main_menu(sockfd)


def main_menu(sockfd):
    sockfd.send("************************* "+Bcolors.FAIL+"MENU"+Bcolors.ENDC+" ***************************\n")
    sockfd.send(Bcolors.FAIL)
    sockfd.send("Escolher Char------------------------------------------(1)\n")
    sockfd.send("Chat---------------------------------------------------(2)\n")
    sockfd.send("Sair---------------------------------------------------(3)\n")
    sockfd.send(Bcolors.OKGREEN)
    sockfd.send("Ver quem esta online-----------------------------------(4)\n")
    sockfd.send(Bcolors.ENDC)
    sockfd.send("**********************************************************\n")
    menu = sockfd.recv(RECV_BUFFER)[:-2]
    if int(menu) == 1:
         choose_char(sockfd)
    if int(menu) == 4:
         online_users(sockfd)


def online_users(sockfd):
    sockfd.send("************************ " +Bcolors.OKGREEN+"USERS"+Bcolors.ENDC+" ***************************\n")
    sockfd.send(Bcolors.OKGREEN)
    for u in User.users:
        sockfd.send('Player:{}\n'.format(u))
    sockfd.send('Total Users:{}\n'.format(len(User.users)))
    sockfd.send(Bcolors.ENDC)
    sockfd.send("**********************************************************\n")
    main_menu(sockfd)


def choose_char(sockfd):
    sockfd.send("**********************"+Bcolors.OKBLUE+" MONTE SEU CHAR "+Bcolors.ENDC+"********************\n")
    sockfd.send(Bcolors.OKBLUE)
    sockfd.send("Escolher Nome------------------------------------------(1)\n")
    sockfd.send("Escolher Classe----------------------------------------(2)\n")
    sockfd.send("Distribuir pontos--------------------------------------(3)\n")
    sockfd.send("Consultar Status---------------------------------------(4)\n")
    sockfd.send("Consultar Inventario-----------------------------------(5)\n")
    sockfd.send(Bcolors.OKBLUE)
    sockfd.send(Bcolors.FAIL)
    sockfd.send("Menu Principal-----------------------------------------(6)\n")
    sockfd.send(Bcolors.ENDC)
    sockfd.send("**********************************************************\n")
    op = sockfd.recv(RECV_BUFFER)[:-2]
    if int(op) == 5:
        main_menu(sockfd)


def cavera(sockfd):
    sockfd.send(
        """                        __________
                      .~#########%%;~.
                     /############%%;`\\
                    /######/~\/~\%%;,; \\
                   |#######\    /;;;;.,.|
                   |#########\/%;;;;;.,.|
          XX       |##/~~\####%;;;/~~\;,|       XX
        XX..X      |#|  o  \##%;/  o  |.|      X..XX
      XX.....X     |##\____/##%;\____/.,|     X.....XX
 XXXXX.....XX      \#########/\;;;;;;,, /      XX.....XXXXX
X |......XX%,.@      \######/%;\;;;;, /      @#%,XX......| X
X |.....X  @#%,.@     |######%%;;;;,.|     @#%,.@  X.....| X
X  \...X     @#%,.@   |# # # % ; ; ;,|   @#%,.@     X.../  X
 X# \.X        @#%,.@                  @#%,.@        X./  #
  ##  X          @#%,.@              @#%,.@          X   #
, "# #X            @#%,.@          @#%,.@            X ##
   `###X             @#%,.@      @#%,.@             ####'
  . ' ###              @#%.,@  @#%,.@              ###`"
    . ";"                @#%.@#%,.@                ;"` ' .
      '                    @#%,.@                   ,.
      ` ,                @#%,.@  @@                `
                          @@@  @@@\n\n"""
    )


def logo(sockfd):
    sockfd.send(
        """
______     _ _  ______ _       _     _     _____
|  ___|   | | | |  ___(_)     | |   | |   |  __ \\
| |_ _   _| | | | |_   _  __ _| |__ | |_  | |  \/ __ _ _ __ ___   ___
|  _| | | | | | |  _| | |/ _` | '_ \| __| | | __ / _` | '_ ` _ \ / _ \\
| | | |_| | | | | |   | | (_| | | | | |_  | |_\ \ (_| | | | | | |  __/
\_|  \__,_|_|_| \_|   |_|\__, |_| |_|\__|  \____/\__,_|_| |_| |_|\___|
                          __/ |
                         |___/

""")


# Function to broadcast messages to all connected clients
def broadcast_data(sock, message, CONNECTION_LIST,  server_socket):
    # Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
