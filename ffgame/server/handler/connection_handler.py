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
    # Handle the case in which there is a new connection recieved through server_socket
    logging.info(f"Client {addr} Connected\n")
    send_message(cavera(), sockfd)
    send_message(Bcolors.OKBLUE, sockfd)
    send_message(logo(), sockfd)
    send_message(Bcolors.ENDC, sockfd)

    while True:
        send_message(Bcolors.ENDC, sockfd)
        send_message("Digite seu Nome e pressione Enter ou Crt-c para Sair\n", sockfd)
        email = sockfd.recv(RECV_BUFFER)[:-2]
        send_message(f"Nome:{email} {Bcolors.FAIL} {Bcolors.ENDC}\nConfirma? s/n? : ", sockfd)
        op = sockfd.recv(RECV_BUFFER)[:-2]
        if op in [b'sim', b's']:
            break
    Char.open(email, sockfd)
    online_users(sockfd, email)
    main_menu(sockfd, email)


def send_message(message, sock):
    if not type(message) == bytes:
        message = message.encode()
        try:
            sock.send(message)
        except Exception as e:
            print(e)

def main_menu(sockfd, perfil_name):
    TITULO = "MENU"
    send_message(
        f"""{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]}\n
        {Bcolors.FAIL} \n
        (1)PERSONAGEM -----------------------------------------------------------------------------------------------------)\n
        {Bcolors.OKGREEN}
        (2)ON-LINE USERS --------------------------------------------------------------------------------------------------)\n
        {Bcolors.WARNING}
        (3)SAIR -----------------------------------------------------------------------------------------------------------)\n
        {Bcolors.ENDC}
        {LINHA}
        """, sockfd)
    while True:
        option = sockfd.recv(RECV_BUFFER)[:-2]
        if option == b"1":
            new_char(sockfd, perfil_name)
        if option == b"2":
            online_users(sockfd, perfil_name)
        if option == b"3":
            send_message(f"{Bcolors.WARNING} Valeu por jogar, volte sempre =)\n Pressione Ctrl+] depois digite quit para sair do telnet\n  {Bcolors.ENDC}", sockfd)
            Char.close(perfil_name, sockfd)
            break
        send_message(f"{Bcolors.FAIL}  Invalid Option\n {Bcolors.ENDC}", sockfd)



def online_users(sockfd, perfil_name):
    TITULO = "USERS"
    send_message(f"{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]} \n", sockfd)
    send_message(Bcolors.OKGREEN, sockfd)
    for user in Char.players:
        send_message(f"Player:{user['player']}\n", sockfd)
    send_message(f"Total:{len(Char.players)}\n", sockfd)
    send_message(Bcolors.ENDC, sockfd)
    main_menu(sockfd, perfil_name)


def char_status(sockfd, perfil_name):
    TITULO = "CHAR POINTS"
    send_message(f"{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]} \n", sockfd)
    send_message(Bcolors.OKGREEN, sockfd)
    char = Char.find_player_by_perfil_name(perfil_name)
    send_message(
        f"""Perfil     :{char.perfil}\n
    (1)Nome       :{char.name}\n
    (2)Força      {char.patk}:[{char.patk * 'I'}]\n
    (3)Defesa     {char.pdef}:[{char.pdef * 'I'}]\n
    (4)Agilidade  0{char.agility}:[{char.agility * 'I'}]\n
    (5)Raiva      0{char.rage}:[{char.rage * 'I'}]\n
    (6)Vitalidade {char.hp}:[{char.hp * 'I'}]\n
    {Bcolors.WARNING}
    Char poins ({char.char_points} : [{char.char_points*'i'}])\n
    {Bcolors.ENDC}
    """, sockfd)
    new_char(sockfd, perfil_name)


def char(sockfd, perfil_name):
    while True:
        TITULO = "PERSONAGEM"
        send_message(
            f"""{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]} \n
            {Bcolors.OKGREEN}
            NOVO PERSONAGEN ***************************************(1)\n
            ESCOLHER JA CRIADO ************************************(2)\n
            VOLTAR ************************************************(3)\n
            {Bcolors.ENDC}
            """, sockfd)

        op = sockfd.recv(RECV_BUFFER)[:-2]
        if op == b'1':
            new_char(sockfd, perfil_name)
            break
        elif op == b'2':
            send_message("EM BREVE ...\n", sockfd)
        elif op == b'3':
            main_menu(sockfd, perfil_name)
            break


def set_name(sockfd, perfil_name):
    while True:
        send_message("Digite o nome do seu personagem, use no maximo 50 letras, nao use espaços eu characters especiais\n", sockfd)
        try:
            name = sockfd.recv(RECV_BUFFER)[:-2]
            char = Char.find_player_by_perfil_name(perfil_name)
            char.name = name
            break
        except Exception as e:
            send_message(f"invalido {e}\n", sockfd)

    new_char(sockfd, perfil_name)


def set_attr(sockfd, perfil_name, maximo, atributo):
    while True:
        send_message(f"Digite o valor para a \033[92m {atributo} \033[0m do seu personagem  MAX = {maximo}\n", sockfd)
        point = int(sockfd.recv(RECV_BUFFER)[:-2])
        if point <= maximo:
            char = Char.find_player_by_perfil_name(perfil_name)
            if char.char_points >= point:
                char.char_points = (char.char_points - point)
                setattr(char, atributo, point)
                break

            else:
                send_message(f"Pontos insuficientes {char.char_points}\n", sockfd)
        else:
            send_message(f"Maximo permitido {maximo}\n", sockfd)

    new_char(sockfd, perfil_name)


def new_char(sockfd, perfil_name):
    TITULO = "NOVO PERSONAGEM"
    char = Char.find_player_by_perfil_name(perfil_name)
    send_message(f"""{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]} \n
    Voce tem {char.char_points} pontos para distribuir entre os atributos do seu personagem, \nfique atento ao valor maximo de cada atributo\n
    {Bcolors.WARNING}
    Perfil        :{char.perfil}\n
    (1)Nome       :{char.name}\n
    {Bcolors.WARNING}
    (2)Força      {char.patk}\n
    {Bcolors.WARNING}
    (3)Defesa     {char.pdef}\n
    {Bcolors.WARNING}
    (4)Agilidade  {char.agility}\n
    {Bcolors.WARNING}
    (5)Raiva      {char.rage}\n
    {Bcolors.WARNING}
    (6)Vitalidade {char.hp}\n
    {Bcolors.ENDC}
    {LINHA}
    {Bcolors.OKBLUE}
    (8) VOLTAR *********************************************************************************************************)\n
    {Bcolors.ENDC}
    (9) JOGAR  *********************************************************************************************************)\n
    {Bcolors.HEADER}
    (10) HELP  *********************************************************************************************************)\n
    {Bcolors.ENDC}
    {LINHA}
    """, sockfd)

    op = sockfd.recv(RECV_BUFFER)[:-2]
    if op == b"1":
        set_name(sockfd, perfil_name)

    elif op == b"2":
        set_attr(sockfd, perfil_name, 35, 'patk')

    elif op == b"3":
        set_attr(sockfd, perfil_name, 35, 'pdef')

    elif op == b"4":
        set_attr(sockfd, perfil_name, 5, 'agility')

    elif op == b"5":
        set_attr(sockfd, perfil_name, 5, 'rage')

    elif op == b"6":
        set_attr(sockfd, perfil_name, 150, 'hp')

    elif op == b"8":
        main_menu(sockfd, perfil_name)

    elif op == b"9":
        p = Char.find_player_by_conn(sockfd)
        Game.start_game(p)

    elif op == b"10":
        help(sockfd, perfil_name)


def help(sockfd, perfil_name):
    TITULO = "AJUDA"
    send_message(f"""{MARGEM} {Bcolors.OKBLUE} {TITULO} {Bcolors.ENDC} {MARGEM[:-len(TITULO)]} \n
    {Bcolors.WARNING}
    (1) Nome       * Define o nome do seu personagem ***********************************************)\n
    (2) Força      * Define a foça bruta do seu golpe ****************************** MAX = 35  *****)\n
    (3) Defesa     * Define a defesa bruta contra golpes sofridos ****************** MAX = 35  *****)\n
    (4) Agilidade  * Melhora porcentagem de chance de desviar de golpes sofridos *** MAX = 5   *****)\n
    (5) Raiva      * Melhora porcentagem de chance de acertar golpes fatais ******** MAX = 5   *****)\n
    (6) Vitalidade * Define a quantidade de pontos de vida do seu personagem (HP)*** MAX = 150 *****)\n
    {Bcolors.ENDC}""", sockfd)
    new_char(sockfd, perfil_name)


def multicast(p1, p2, message):
    p1.send(message)
    p2.send(message)


def cavera():
    return """
                         __________
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


def logo():
    return """
______     _ _  ______ _       _     _     _____
|  ___|   | | | |  ___(_)     | |   | |   |  __ \\
| |_ _   _| | | | |_   _  __ _| |__ | |_  | |  \/ __ _ _ __ ___   ___
|  _| | | | | | |  _| | |/ _` | '_ \| __| | | __ / _` | '_ ` _ \ / _ \\
| | | |_| | | | | |   | | (_| | | | | |_  | |_\ \ (_| | | | | | |  __/
\_|  \__,_|_|_| \_|   |_|\__, |_| |_|\__|  \____/\__,_|_| |_| |_|\___|
                          __/ |
                         |___/

"""


def chance(probability):
    return random.randrange(100) < probability


def hit_pvp(p1, p2):
    if chance(90 - p1['char'].agility):
        if chance(10 + p2['char'].rage):
            multicast(p1['conn'], p2['conn'], p1['char'].hit(p2['char'].patk, p2['char'].name, 2))
            if p1['char'].is_dead():
                # multicast(p1['conn'], p2['conn'], f"{Bcolors.FAIL} VENCEDOR: {p2['char'].name} HP:({p2['char'].hp}) {Bcolors.ENDC}")
                return True
        else:
            multicast(p1['conn'], p2['conn'], p1['char'].hit(p2['char'].patk, p2['char'].name))
            if p1['char'].is_dead():
                # multicast(p1['conn'], p2['conn'], f"{Bcolors.FAIL} VENCEDOR: {p2['char'].name} HP:({p2['char'].hp}) {Bcolors.ENDC}")
                return True
    else:
        multicast(p1['conn'], p2['conn'], f"{Bcolors.FAIL} {p2['char'].name} ERRRRRROOOUUU!!! {Bcolors.ENDC}")
        return False


def start_fight(p1, p2):
    multicast(p1['conn'], p2['conn'], f"{MARGEM} {INICIO} {MARGEM}")
    multicast(p1['conn'], p2['conn'], f"{Bcolors.OKBLUE} {p1['char'].status()}")
    multicast(p1['conn'], p2['conn'], f"{Bcolors.OKGREEN} {p2['char'].status()} {Bcolors.ENDC}")


def fight(p1, p2, i):
    multicast(p1['conn'], p2['conn'], f"{MARGEM} Jogada {i} {MARGEM}")

    if i % 2 == 0:
        time.sleep(2)
        if hit_pvp(p1, p2):
            return True
    else:
        time.sleep(3)
        if hit_pvp(p2, p1):
            return True

    multicast(p1['conn'], p2['conn'], LINHA)
    multicast(p1['conn'], p2['conn'], f"{Bcolors.OKBLUE} {p1['char'].status()}")
    multicast(p1['conn'], p2['conn'], f"{Bcolors.OKGREEN} {p2['char'].status()} {Bcolors.ENDC}")


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
        send_message("Aguarde seu oponente...", cls.players[0]['conn'])

        if cls.players.__len__() == 2:
            send_message("Arena iniciada...\n", cls.players[0]['conn'])
            send_message(f"{cls.players[0]['char'].name} X {cls.players[1]['char'].name}", cls.players[0]['conn'])
            send_message("Arena iniciada...\n", cls.players[1]['conn'])
            send_message(f"{cls.players[0]['char'].name} X {cls.players[1]['char'].name}", cls.players[1]['conn'])
            send_message("Consultando Oraculo para ver quem começa...\n", cls.players[0]['conn'])

            p1 = cls.players[0] if random.randint(1, 100) < 50 else cls.players[1]
            if cls.players[0] == p1:
                p2 = cls.players[1]
            else:
                p2 = cls.players[0]

            send_message(f"P1:{p1['char'].name} x P2:{p2['char'].name}\n", cls.players[0]['conn'])
            send_message(f"P1:{p1['char'].name} x P2:{p2['char'].name}\n", cls.players[1]['conn'])
            send_message(f"P1:{p1['char'].name} Comeca....\n", cls.players[0]['conn'])
            send_message(f"P1:{p2['char'].name} Comeca....\n", cls.players[1]['conn'])

            start_fight(p1, p2)

            send_message("Voce Comeca....\n", p1['conn'])
            send_message("Aguarde a Jogada....\n", p2['conn'])

            for i in range(1, 50):
                if fight(p1, p2, i):
                    break
