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
        logging.info(f'Player Login: {perfil}')
        print(f'Connected Users {str(len(Char.players))} Last Player: {perfil}')

    @classmethod
    def close(cls, perfil, conn):
        for user in cls.players:
            if user['player'] == perfil:
                #conn.close()
                cls.players.remove(u)
                logging.info(f"Player Logout: {perfil}")
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
            return f"{name} >-----> {self.name} < {power}"
        else:
            power = (patk - self.pdef)
            self.hp = (self.hp - power)
            return f"{name} >-----> {self.name} < {power}"

    def status(self):
        return f"{self.name}({self.hp}):HP {self.hp * '#'}"

    def is_dead(self):
        return self.hp <= 0
