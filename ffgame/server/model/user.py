#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Class to mantein a dict users in memory
"""
import logging
from utils.colors import Bcolors


class Char:

    players = []

    def __init__(self, perfil):
        self.perfil = perfil
        self.name = None
        self.hp = 0
        self.pdef = 0
        self.patk = 0
        self.agility = 0
        self.rage = 0
        self.ready = False
        self.char_points = 150

    @classmethod
    def open(cls, perfil, conn):
        char = Char(perfil)
        cls.players.append({"player": perfil, "char": char, "conn": conn})
        logging.info('Player Login: {}'.format(perfil))
        print(f'Connected Users {str(len(Char.players))} Last Player: {perfil}')

    @classmethod
    def close(cls, perfil, conn):
        for u in cls.players:
            if u['player'] == perfil:
                #conn.close()
                cls.players.remove(u)
                logging.info("Player Logout: {}".format(perfil))
                break

    @classmethod
    def find_player_by_perfil_name(cls, perfil_name):
        return [p['char'] for p in cls.players if p['player'] == perfil_name][0]

    @classmethod
    def find_conn_by_perfil_name(cls, perfil_name):
        return [p['conn'] for p in cls.players if p['player'] == perfil_name][0]

    @classmethod
    def find_player_by_conn(cls, conn):
        return [p for p in cls.players if p['conn'] == conn][0]

    def hit(self, patk, name, crit=None):
        if crit:
            power = ((patk * crit) - self.pdef)
            self.hp = (self.hp - power)
            return Bcolors.ENDC + "{} "'\033[93m'" >-----> "'\033[0m'"{} <"'\033[95m'"(-{}) "'\033[0m'"critical>".format(name,self.name, power) + Bcolors.ENDC
        else:
            power = (patk - self.pdef)
            self.hp = (self.hp - power)
            return Bcolors.ENDC+"{} "'\033[92m'" >-----> "'\033[0m'"{} <"'\033[91m'"(-{}) "'\033[0m'"hit>".format(name, self.name, power) +Bcolors.ENDC

    def status(self):
        return "{}({}):HP {}".format(self.name, self.hp, (self.hp * '#'))

    def is_dead(self):
        return self.hp <= 0
