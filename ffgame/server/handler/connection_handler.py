# -*- coding: utf-8 -*-
"""
 Class to manage bussines requests
"""
import random
import time

from model.user import Char
from model.arena import Arena
from utils.style import (
    LINHA,
    MARGEM,
    cavera,
    logo,
    Colors,
    first_menu,
    char_set_menu,
    welcome,
    name_message,
    confirm_message,
    bye_message,
    invalid_option,
    help_menu
)

from utils.utils import receive_message, send_message


def login(sockfd):
    send_message(welcome, sockfd)
    while True:
        send_message(name_message, sockfd)
        username = receive_message(sockfd)
        send_message(confirm_message(username), sockfd)
        op = receive_message(sockfd)
        if op.lower() in ["sim", "s"]:
            break

    char = Char(username)
    Arena.add_user(username, sockfd, char)
    online_users(sockfd, username)
    main_menu(sockfd, username)


def main_menu(sockfd, perfil_name):
    send_message(first_menu("MENU"), sockfd)
    while True:
        option = receive_message(sockfd)
        if option == "1":
            new_char(sockfd, perfil_name)
        if option == "2":
            online_users(sockfd, perfil_name)
        if option == "3":
            send_message(bye_message, sockfd)
            Char.close(perfil_name, sockfd)
            break
        send_message(invalid_option, sockfd)


def online_users(sockfd, perfil_name):
    TITULO = "USERS"
    send_message(
        f"{MARGEM} {Colors.OKBLUE} {TITULO} {Colors.ENDC} {MARGEM[:-len(TITULO)]} \n",
        sockfd,
    )
    send_message(Colors.OKGREEN, sockfd)
    for user in Arena.players:
        send_message(f"Player:{user}\n", sockfd)
    send_message(f"Total:{len(Arena.players)}\n", sockfd)
    send_message(Colors.ENDC, sockfd)
    main_menu(sockfd, perfil_name)


def char_status(sockfd, perfil_name):
    TITULO = "CHAR POINTS"
    send_message(
        f"{MARGEM} {Colors.OKBLUE} {TITULO} {Colors.ENDC} {MARGEM[:-len(TITULO)]} \n",
        sockfd,
    )
    send_message(Colors.OKGREEN, sockfd)
    char = Char.find_player_by_perfil_name(perfil_name)
    send_message(
        f"""Perfil     :{char.perfil}\n
    (1)Nome       :{char.name}\n
    (2)Força      {char.patk}:[{char.patk * 'I'}]\n
    (3)Defesa     {char.pdef}:[{char.pdef * 'I'}]\n
    (4)Agilidade  0{char.agility}:[{char.agility * 'I'}]\n
    (5)Raiva      0{char.rage}:[{char.rage * 'I'}]\n
    (6)Vitalidade {char.hp}:[{char.hp * 'I'}]\n
    {Colors.WARNING}
    Char poins ({char.skill_points} : [{char.skill_points*'i'}])\n
    {Colors.ENDC}
    """,
        sockfd,
    )
    new_char(sockfd, perfil_name)


def char(sockfd, perfil_name):
    while True:
        TITULO = "PERSONAGEM"
        send_message(
            f"""{MARGEM} {Colors.OKBLUE} {TITULO} {Colors.ENDC} {MARGEM[:-len(TITULO)]} \n
            {Colors.OKGREEN}
            NOVO PERSONAGEN ***************************************(1)\n
            ESCOLHER JA CRIADO ************************************(2)\n
            VOLTAR ************************************************(3)\n
            {Colors.ENDC}
            """,
            sockfd,
        )

        op = receive_message(sockfd)
        if op == "1":
            new_char(sockfd, perfil_name)
            break
        elif op == "2":
            send_message("EM BREVE ...\n", sockfd)
        elif op == "3":
            main_menu(sockfd, perfil_name)
            break


def set_name(sockfd, username):
    while True:
        send_message(
            "Digite o nome do seu personagem, use no maximo 50 letras, nao use espaços eu characters especiais\n",
            sockfd,
        )
        try:
            name = receive_message(sockfd)
            player = Arena.get_user(username)
            player['char'].name = name
            break
        except Exception as e:
            send_message(f"Invalido {e}\n", sockfd)

    new_char(sockfd, username)


def set_attr(sockfd, username, maximo, atributo):
    while True:
        send_message(
            f"Digite o valor para a \033[92m {atributo} \033[0m do seu personagem  MAX = {maximo}\n",
            sockfd,
        )
        point = int(receive_message(sockfd))
        if point <= maximo:
            player = Arena.get_user(username)
            if player['char'].skill_points >= point:
                player['char'].skill_points -= point
                setattr(player['char'], atributo, point)
                break

            else:
                send_message(f"Pontos insuficientes {player['char'].skill_points}\n", sockfd)
        else:
            send_message(f"Maximo permitido {maximo}\n", sockfd)

    new_char(sockfd, username)


def new_char(sockfd, username):
    TITULO = "NOVO PERSONAGEM"
    player = Arena.get_user(username)
    send_message(char_set_menu(player['char'], TITULO), sockfd)

    op = receive_message(sockfd)
    if op == "1":
        set_name(sockfd, username)

    elif op == "2":
        set_attr(sockfd, username, 35, "p_atk")

    elif op == "3":
        set_attr(sockfd, username, 35, "p_def")

    elif op == "4":
        set_attr(sockfd, username, 5, "agility")

    elif op == "5":
        set_attr(sockfd, username, 5, "rage")

    elif op == "6":
        set_attr(sockfd, username, 150, "hp")

    elif op == "8":
        main_menu(sockfd, username)

    elif op == "9":
        player = Arena.get_user(username)
        Game.start_game(player)

    elif op == "10":
        help(sockfd, username)


def help(sockfd, perfil_name):
    send_message(help_menu("AJUDA"), sockfd)
    new_char(sockfd, perfil_name)


def multicast(p1, p2, message):
    send_message(message, p1['conn'])
    send_message(message, p2['conn'])


def chance(probability):
    return random.randrange(100) < probability


def hit_pvp(atack, defence):
    if chance(80 - defence['char'].agility):
            power = (atack['char'].f_hit() - defence['char'].p_def)
            defence['char'].hp -= power
            multicast(atack, defence, f"{atack['char'].name} --attack--> {defence['char'].name} power: {power}")
            if defence['char'].is_dead():
                multicast(atack, defence, f"{Colors.FAIL} VENCEDOR: {atack['char'].name} HP:({atack['char'].hp}) {Colors.ENDC}\n")
                return True
            return False
    else:
        multicast(atack, defence, f"{Colors.FAIL} {atack['char'].name} ERRRRRROOOUUU!!! {Colors.ENDC}\n")
        return False


def start_fight(p1, p2):
    multicast(p1, p2, f"{MARGEM} INICIO {MARGEM}\n")
    multicast(p1, p2, f"{Colors.OKBLUE} {p1['char'].status()}\n")
    multicast(p1, p2, f"{Colors.OKGREEN} {p2['char'].status()} {Colors.ENDC}\n")


def fight(p1, p2, i):
    multicast(p1, p2, f"{MARGEM} Jogada {i} {MARGEM}\n")

    if i % 2 == 0:
        time.sleep(2)
        if hit_pvp(p1, p2):
            return True
    else:
        time.sleep(3)
        if hit_pvp(p2, p1):
            return True

    multicast(p1, p2, LINHA)
    multicast(p1, p2, f"{Colors.OKBLUE} {p1['char'].status()}\n")
    multicast(p1, p2, f"{Colors.OKGREEN} {p2['char'].status()} {Colors.ENDC}\n")


# Function to broadcast messages to all connected clients
def broadcast_data(sock, message, CONNECTION_LIST, server_socket):
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
        send_message("Aguarde seu oponente...\n", player['conn'])

        if cls.players.__len__() == 2:
            send_message("Arena iniciada...\n", player['conn'])
            send_message(
                f"{cls.players[0]['char'].name} X {cls.players[1]['char'].name}",
                cls.players[0]["conn"],
            )
            send_message("Arena iniciada...\n", cls.players[1]["conn"])
            send_message(
                f"{cls.players[1]['char'].name} X {cls.players[0]['char'].name}\n",
                cls.players[1]["conn"],
            )
            send_message(
                "Consultando Oraculo para ver quem começa...\n", cls.players[0]["conn"]
            )

            p1 = cls.players[0] if random.randint(1, 100) < 50 else cls.players[1]
            if cls.players[0] == p1:
                p2 = cls.players[1]
            else:
                p2 = cls.players[0]

            send_message(f"P1: {p1['char'].name} Comeca....\n", p1["conn"])
            send_message(f"P1: {p1['char'].name} Comeca....\n", p2["conn"])

            start_fight(p1, p2)

            send_message("Voce Comeca....\n", p1["conn"])
            send_message("Aguarde a Jogada....\n", p2["conn"])

            for i in range(1, 50):
                if fight(p1, p2, i):
                    break
