#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Class to mantein a dict users in memory
"""
import logging


class Char:

    players = []

    def __init__(self, perfil_name):
        self.perfil_name = perfil_name
        self.char_name = None
        self.classe = None
        self.classe_points = 35
        self.f_attack = 0
        self.m_attack = 0
        self.f_def = 0
        self.m_def = 0
        self.hp_multiplier = 0
        self.mp_multiplier = 0
        self.mp = 100
        self.hp = 100
        self.armor = None
        self.inventory = None
        self.weapon = None

    @classmethod
    def open(cls, perfil_name, conn):
        char = Char(perfil_name)
        cls.players.append({"player": perfil_name, "char": char, "conn": conn})
        print cls.players
        logging.info('Player Login: {}'.format(perfil_name))
        print 'Connected Users (+)'+str(len(Char.players))+' Last Player: '+perfil_name

    @classmethod
    def close(cls, user):
       pass

    @classmethod
    def find_player_by_perfil_name(cls, perfil_name):
        return [p['char'] for p in cls.players if p['player'] == perfil_name]

    @classmethod
    def find_conn_by_perfil_name(cls, perfil_name):
        return [p['conn'] for p in cls.players if p['player'] == perfil_name]
