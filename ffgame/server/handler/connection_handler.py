# -*- coding: utf-8 -*-
"""
 Class to manage bussines requests
"""
import logging
from model.user import Char

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
        sockfd.send("Digite seu Nome e pressione Enter ou Crt-c para Sair\n")
        email = sockfd.recv(RECV_BUFFER)[:-2]
        sockfd.send("Nome:"+Bcolors.FAIL+" {}\nConfirma? s/n? ".format(email)+Bcolors.ENDC)
        op = sockfd.recv(RECV_BUFFER)[:-2]
        if op == 's':
            option = op
    Char.open(email, sockfd)
    online_users(sockfd, email)
    main_menu(sockfd, email)


def main_menu(sockfd, perfil_name):
    op = 4
    sockfd.send("************************* "+Bcolors.FAIL+"MENU"+Bcolors.ENDC+" ***************************\n")
    sockfd.send(Bcolors.FAIL)
    sockfd.send("Criar Personagem---------------------------------------(1)\n")
    sockfd.send(Bcolors.OKGREEN)
    sockfd.send("Ver quem esta online-----------------------------------(2)\n")
    sockfd.send(Bcolors.WARNING)
    sockfd.send("Sair---------------------------------------------------(3)\n")
    sockfd.send(Bcolors.ENDC)
    sockfd.send("**********************************************************\n")

    while op >= 4:
        menu = sockfd.recv(RECV_BUFFER)[:-2]
        try:
            int(menu)
        except ValueError:
            sockfd.send(Bcolors.FAIL+"Invalid Option\n"+Bcolors.ENDC)
            #main_menu(sockfd, perfil_name)
            break
        if menu != '' and int(menu) < op:
            op = int(menu)
            if op == 1:
                choose_char(sockfd, perfil_name)
            if op == 2:
                online_users(sockfd, perfil_name)
            if op == 3:
                sockfd.send(Bcolors.WARNING + "Valeu por jogar, volte sempre =)\n"
                                              "Pressione Ctrl+] depois digite quit para sair do telnet\n" + Bcolors.ENDC)
                Char.close(perfil_name, sockfd)
                break

        else:
            try:
                sockfd.send(Bcolors.FAIL+"Invalid Option\n"+Bcolors.ENDC)
                main_menu(sockfd, perfil_name)
            except Exception:
                break
                pass


def online_users(sockfd, perfil_name):
    sockfd.send("************************ " +Bcolors.OKGREEN+"USERS"+Bcolors.ENDC+" ***************************\n")
    sockfd.send(Bcolors.OKGREEN)
    for u in Char.players:
        sockfd.send('Player:{}\n'.format(u['player']))
    sockfd.send('Total:{}\n'.format(len(Char.players)))
    sockfd.send(Bcolors.ENDC)
    main_menu(sockfd, perfil_name)


def char_status(sockfd, perfil_name):
    sockfd.send("************************ " +Bcolors.OKGREEN+"CHAR POINTS"+Bcolors.ENDC+" ***************************\n")
    sockfd.send(Bcolors.OKGREEN)
    char = Char.find_player_by_perfil_name(perfil_name)
    sockfd.send("Perfil Name *******************************************({})\n".format(char.perfil_name))
    sockfd.send("Char Name *********************************************({})\n".format(char.char_name))
    sockfd.send("Char Points *******************************************({})\n".format(char.classe_points))
    sockfd.send("Classe ************************************************({})\n".format(char.classe))
    sockfd.send("Fisical Attack ****************************************({})\n".format(char.f_attack))
    sockfd.send("Fisical Defence ***************************************({})\n".format(char.f_def))
    sockfd.send("Magical Attack ****************************************({})\n".format(char.m_attack))
    sockfd.send("Magical Defence ***************************************({})\n".format(char.m_def))
    sockfd.send("Healling Points ***************************************({})\n".format(char.hp))
    sockfd.send("Mana Points *******************************************({})\n".format(char.mp))
    sockfd.send("Armor *************************************************({})\n".format(char.armor))
    sockfd.send("Weapon ************************************************({})\n".format(char.weapon))
    sockfd.send(Bcolors.ENDC)
    main_menu(sockfd, perfil_name)


def choose_char(sockfd, perfil_name):
    op = 7
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
    while op >= 7:
        menu = sockfd.recv(RECV_BUFFER)[:-2]
        if menu != '' and int(menu) < 7:
            op = int(menu)
            if op == 1:
                choose_char(sockfd, perfil_name)
                break
            if op == 6:
                main_menu(sockfd, perfil_name)
                break
            if op == 4:
                char_status(sockfd, perfil_name)

        else:
            sockfd.send(Bcolors.FAIL+"Invalid Option\n"+Bcolors.ENDC)


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
