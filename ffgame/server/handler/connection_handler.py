# -*- coding: utf-8 -*-
"""
 Class to manage bussines requests
"""
import json
import logging
import random

import time
from utils.colors import Bcolors
from model.user import Char

RECV_BUFFER = 4096
MARGEM = (58*"*")
LINHA = (116*"*"+"\n")


def login(addr, sockfd):
    option = 'n'
    # Handle the case in which there is a new connection recieved through server_socket
    logging.info("Client {} Connected".format(addr))
    cavera(sockfd)
    sockfd.send(Bcolors.OKBLUE)
    logo(sockfd)
    sockfd.send(Bcolors.ENDC)
    while True:
        sockfd.send("Digite seu Nome e pressione Enter ou Crt-c para Sair\n".encode())
        email = sockfd.recv(RECV_BUFFER)[:-2]
        sockfd.send("Nome:{email} {Bcolors.FAIL} {Bcolors.ENDC}\nConfirma? s/n? ".encode())
        op = sockfd.recv(RECV_BUFFER)[:-2]
        if op == b's':
            break
    Char.open(email, sockfd)
    online_users(sockfd, email)
    main_menu(sockfd, email)


def main_menu(sockfd, perfil_name):
    TITULO = " MENU "
    op = 4
    sockfd.send(f"{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]} \n".encode())
    sockfd.send(Bcolors.FAIL)
    sockfd.send("(1)PERSONAGEM -----------------------------------------------------------------------------------------------------)\n".encode())
    sockfd.send(Bcolors.OKGREEN)
    sockfd.send("(2)ON-LINE USERS --------------------------------------------------------------------------------------------------)\n".encode())
    sockfd.send(Bcolors.WARNING)
    sockfd.send("(3)SAIR -----------------------------------------------------------------------------------------------------------)\n".encode())
    sockfd.send(Bcolors.ENDC)
    sockfd.send(LINHA.encode())

    while op >= 4:
        menu = sockfd.recv(RECV_BUFFER)[:-2]
        try:
            int(menu)
        except ValueError:
            sockfd.send(Bcolors.FAIL+"Invalid Option\n"+Bcolors.ENDC)
            pass
        if menu != '' and int(menu) < op:
            op = int(menu)
            if op == 1:
                new_char(sockfd, perfil_name)
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
            except Exception:
                pass


def online_users(sockfd, perfil_name):
    TITULO = "USERS "
    sockfd.send(f"{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]} \n".encode())
    sockfd.send(Bcolors.OKGREEN)
    for u in Char.players:
        sockfd.send(f"Player:{u['player']}\n".encode())
    sockfd.send(f"Total:{len(Char.players)}\n".encode())
    sockfd.send(Bcolors.ENDC)
    main_menu(sockfd, perfil_name)


def char_status(sockfd, perfil_name):
    TITULO = " CHAR POINTS "
    sockfd.send(f"{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]} \n".encode())
    sockfd.send(Bcolors.OKGREEN)
    char = Char.find_player_by_perfil_name(perfil_name)
    sockfd.send("Perfil     :{}\n".format(char.perfil))
    sockfd.send("(1)Nome       :{}\n".format(char.name))
    sockfd.send("(2)Força      {}:[".format(char.patk) + char.patk*'I'+"]\n")
    sockfd.send("(3)Defesa     {}:[".format(char.pdef) + char.pdef*'I'+"]\n")
    sockfd.send("(4)Agilidade  0{}:[".format(char.agility) + char.agility*'I'+"]\n")
    sockfd.send("(5)Raiva      0{}:[".format(char.rage) + char.rage*'I'+"]\n")
    sockfd.send("(6)Vitalidade {}:[".format(char.hp) + char.hp*'I'+"]\n")
    sockfd.send(Bcolors.WARNING)
    sockfd.send("Char poins ({})".format(char.char_points) + char.char_points*'i'+")\n")
    sockfd.send(Bcolors.ENDC)
    new_char(sockfd, perfil_name)


def char(sockfd, perfil_name):

    while True:
        TITULO = " PERSONAGEM "
        sockfd.send(f"{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]} \n".encode())
        sockfd.send(Bcolors.OKGREEN)
        sockfd.send("NOVO PERSONAGEN ***************************************(1)\n")
        sockfd.send("ESCOLHER JA CRAIDO ************************************(2)\n")
        sockfd.send("VOLTAR ************************************************(3)\n")
        sockfd.send(Bcolors.ENDC)

        op = int(sockfd.recv(RECV_BUFFER)[:-2])

        if op == 1:
            new_char(sockfd, perfil_name)
            break
        elif op == 2:
            sockfd.send("EM BREVE ...\n")
        elif op == 3:
            main_menu(sockfd, perfil_name)
            break


def set_name(sockfd, perfil_name):
    while True:
        sockfd.send("Digite o nome do seu personagem, use no maximo 50 letras, nao use espaços eu characters especiais\n".encode())
        try:
            name = sockfd.recv(RECV_BUFFER)[:-2]
            char = Char.find_player_by_perfil_name(perfil_name)
            char.name = name
            break
        except Exception as e:
            sockfd.send("invalido {}\n".format(e))
            pass

    new_char(sockfd, perfil_name)


def set_attr(sockfd, perfil_name, maximo, atributo):
    while True:
        sockfd.send(f"Digite o valor para a "'\033[92m'" {atributo} "'\033[0m'" do seu personagem  MAX = {maximo}\n".encode())
        point = int(sockfd.recv(RECV_BUFFER)[:-2])
        if point <= maximo:
            char = Char.find_player_by_perfil_name(perfil_name)
            if char.char_points >= point:
                char.char_points = (char.char_points - point)
                setattr(char, atributo, point)
                break

            else:
                sockfd.send(f"Pontos insuficientes {char.char_points}\n".encode())
        else:
            sockfd.send(f"Maximo permitido {maximo}\n".encode())
    new_char(sockfd, perfil_name)


def new_char(sockfd, perfil_name):
    char = Char.find_player_by_perfil_name(perfil_name)
    TITULO = "NOVO PERSONAGEM "
    sockfd.send(f"{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]} \n".encode())
    sockfd.send(f"Voce tem {char.char_points} pontos para distribuir entre os atributos do seu personagem, \nfique atento ao valor maximo de cada atributo\n".encode())
    sockfd.send(Bcolors.WARNING)
    sockfd.send(f"Perfil        :{char.perfil}\n".encode())
    sockfd.send(f"(1)Nome       :{'033[91m'} {char.name}\n".encode())
    sockfd.send(Bcolors.WARNING)
    sockfd.send("(2)Força      {}:["'\033[92m'"".format(char.patk) + char.patk * 'I' + Bcolors.WARNING+"]\n".encode())
    sockfd.send(Bcolors.WARNING)
    sockfd.send("(3)Defesa     {}:["'\033[92m'"".format(char.pdef) + char.pdef * 'I' + Bcolors.WARNING+"]\n".encode())
    sockfd.send(Bcolors.WARNING)
    sockfd.send("(4)Agilidade  0{}:["'\033[92m'"".format(char.agility) + char.agility * 'I' + Bcolors.WARNING+"]\n".encode())
    sockfd.send(Bcolors.WARNING)
    sockfd.send("(5)Raiva      0{}:["'\033[92m'"".format(char.rage) + char.rage * 'I' + Bcolors.WARNING+"]\n".encode())
    sockfd.send(Bcolors.WARNING)
    sockfd.send("(6)Vitalidade {}:["'\033[92m'"".format(char.hp) + char.hp * 'I' + Bcolors.WARNING+"]\n".encode())
    sockfd.send(Bcolors.ENDC)
    sockfd.send(LINHA)
    sockfd.send(Bcolors.OKBLUE)
    sockfd.send("(8) VOLTAR *********************************************************************************************************)\n".encode())
    sockfd.send(Bcolors.ENDC)
    sockfd.send("(9) JOGAR  *********************************************************************************************************)\n".encode())
    sockfd.send(Bcolors.HEADER)
    sockfd.send("(10) HELP  *********************************************************************************************************)\n".encode())
    sockfd.send(Bcolors.ENDC)
    sockfd.send(LINHA)

    op = int(sockfd.recv(RECV_BUFFER)[:-2])
    if op == 1:
        set_name(sockfd, perfil_name)

    elif op == 2:
        set_attr(sockfd, perfil_name, 35, 'patk')

    elif op == 3:
        set_attr(sockfd, perfil_name, 35, 'pdef')

    elif op == 4:
        set_attr(sockfd, perfil_name, 5, 'agility')

    elif op == 5:
        set_attr(sockfd, perfil_name, 5, 'rage')

    elif op == 6:
        set_attr(sockfd, perfil_name, 150, 'hp')

    elif op == 8:
        main_menu(sockfd, perfil_name)

    elif op == 9:
        p = Char.find_player_by_conn(sockfd)
        Game.start_game(p)

    elif op == 10:
        help(sockfd, perfil_name)


def help(sockfd, perfil_name):
    TITULO = " AJUDA "
    sockfd.send(MARGEM + Bcolors.OKBLUE + TITULO + Bcolors.ENDC + (MARGEM[:-len(TITULO)]) + "\n".encode())
    sockfd.send(Bcolors.WARNING)
    sockfd.send("(1) Nome       * Define o nome do seu personagem ***********************************************)\n".encode())
    sockfd.send("(2) Força      * Define a foça bruta do seu golpe ****************************** MAX = 35  *****)\n".encode())
    sockfd.send("(3) Defesa     * Define a defesa bruta contra golpes sofridos ****************** MAX = 35  *****)\n".encode())
    sockfd.send("(4) Agilidade  * Melhora porcentagem de chance de desviar de golpes sofridos *** MAX = 5   *****)\n".encode())
    sockfd.send("(5) Raiva      * Melhora porcentagem de chance de acertar golpes fatais ******** MAX = 5   *****)\n".encode())
    sockfd.send("(6) Vitalidade * Define a quantidade de pontos de vida do seu personagem (HP)*** MAX = 150 *****)\n".encode())
    sockfd.send(Bcolors.ENDC)
    new_char(sockfd, perfil_name)


def multicast(p1, p2, message):
    p1.send(message+"\n")
    p2.send(message+"\n")


def cavera(sockfd):
    sockfd.send(
"""                      __________
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
                          @@@  @@@\n\n""".encode()
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

""".encode())


def chance(probability):
    return random.randrange(100) < probability


def hit_pvp(p1, p2):
    if chance(90 - p1['char'].agility):
        if chance(10 + p2['char'].rage):
            multicast(p1['conn'], p2['conn'], p1['char'].hit(p2['char'].patk, p2['char'].name, 2))
            if p1['char'].is_dead():
                multicast(p1['conn'], p2['conn'], Bcolors.FAIL + "VENCEDOR: {} HP:({})".format(p2['char'].name, p2['char'].hp) +Bcolors.ENDC)
                return True
        else:
            multicast(p1['conn'], p2['conn'], p1['char'].hit(p2['char'].patk, p2['char'].name))
            if p1['char'].is_dead():
                multicast(p1['conn'], p2['conn'], Bcolors.FAIL + "VENCEDOR: {} HP:({})".format(p2['char'].name, p2['char'].hp) + Bcolors.ENDC)
                return True
    else:
        multicast(p1['conn'], p2['conn'], Bcolors.FAIL + "{} ERRRRRROOOUUU!!!".format(p2['char'].name) + Bcolors.ENDC)
        return False


def start_fight(p1, p2):
    multicast(p1['conn'], p2['conn'], MARGEM+" INICIO "+MARGEM)
    multicast(p1['conn'], p2['conn'], Bcolors.OKBLUE + p1['char'].status())
    multicast(p1['conn'], p2['conn'], Bcolors.OKGREEN + p2['char'].status() + Bcolors.ENDC)


def fight(p1, p2, i):
    multicast(p1['conn'], p2['conn'], MARGEM+" Jogada {} ".format(i)+MARGEM)

    if i % 2 == 0:
        time.sleep(2)
        if hit_pvp(p1, p2):
            return True
    else:
        time.sleep(3)
        if hit_pvp(p2, p1):
            return True

    multicast(p1['conn'], p2['conn'], LINHA)
    multicast(p1['conn'], p2['conn'], Bcolors.OKBLUE + p1['char'].status())
    multicast(p1['conn'], p2['conn'], Bcolors.OKGREEN + p2['char'].status() + Bcolors.ENDC)


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


class Game:
    players = []

    @classmethod
    def start_game(cls, player):

        cls.players.append(player)
        cls.players[0]['conn'].send(b"Aguarde seu oponente...")

        if cls.players.__len__() >= 2:
            cls.players[0]['conn'].send(b"Arena iniciada...\n")
            cls.players[0]['conn'].send(b"{} x {}\n".format(cls.players[0]['char'].name, cls.players[1]['char'].name))
            cls.players[1]['conn'].send(b"Arena iniciada...\n")
            cls.players[1]['conn'].send(b"{} x {}\n".format(cls.players[0]['char'].name, cls.players[1]['char'].name))
            cls.players[0]['conn'].send("Consultando Oraculo para ver quem começa...\n".encode())

            p1 = cls.players[0] if random.randint(1, 100) < 50 else cls.players[1]
            if cls.players[0] == p1:
                p2 = cls.players[1]
            else:
                p2 = cls.players[0]

            cls.players[0]['conn'].send(b"P1:{} x P2:{}\n".format(p1['char'].name, p2['char'].name))
            cls.players[1]['conn'].send(b"P1:{} x P2:{}\n".format(p1['char'].name, p2['char'].name))
            cls.players[0]['conn'].send(b"P1:{} Comeca....\n".format(p1['char'].name))
            cls.players[1]['conn'].send(b"P1:{} Comeca....\n".format(p1['char'].name))

            start_fight(p1, p2)

            p1['conn'].send(b"Voce Comeca....\n")
            p2['conn'].send(b"Aguarde a Jogada....\n")

            for i in range(1, 50):
                if fight(p1, p2, i):
                    break
