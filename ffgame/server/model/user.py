#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import time
import logging


class User:

    users = []

    def __init__(self, connection_id):
        self.start_time = time.time()
        self.connection_id = connection_id
        self.name = None

    @classmethod
    def open(cls, sock, user_obj):
        u = User(sock)
        u.iss = user_obj.iss
        u.network = user_obj.network
        u.exp = user_obj.exp
        u.username = user_obj.username
        u.displayname = user_obj.displayname
        u.resource = user_obj.resource
        u.networkId = user_obj.networkId
        u.status = 1

        cls.users.append(u)
        # logging.info("number on itens: %r", len(cls.users))
        print 'connections (+)'+str(len(User.users))+' User: '+u.username

    @classmethod
    def close(cls, sock):
        user_close = None
        for el in User.users:
            if el.connection == sock:
                user_close = el.displayname
                el.connection.close()
                cls.users.remove(el)
                print 'connection (-)'+str(len(User.users))+' User: '+el.username
                break
        return user_close

    @classmethod
    def find_user_by_name(cls, _name, audience):
        user_found = None
        for waiter in cls.users:
            if (waiter.username == _name) and (waiter.resource == audience):
                user_found = waiter
                break
        return user_found

    @classmethod
    def find_network_by_sock(cls, sock):
        net_found = None
        for waiter in cls.users:
            if waiter.connection == sock:
                net_found = waiter.resource
                break
        return net_found

    @classmethod
    def find_user_by_sock(cls, sock):
        user_found = None
        for waiter in cls.users:
            if waiter.connection == sock:
                user_found = waiter
                break
        return user_found

    @classmethod
    def who_online_by_net(cls, network):
        res = []

        for u in User.users:
            if network == u.resource:
                res.append({'user_name': u.username, 'status': u.status})

        '''
        1: 'profile__status--disponivel',
        2: 'profile__status--ocupado',
        3: 'profile__status--ausente',
        4: 'profile__status--offline'
        '''
        return res

    @classmethod
    def supervisor(cls):

        network_list = []
        network = {}
        temp_network = {}

        for u in User.users:
            if u.network not in network_list:
                network_list.append(u.network)
                temp_network[u.network] = 1
            else:
                temp_network[u.network] += 1

        amount = len(User.users)
        network["total"] = amount
        network["network"] = temp_network

        return network

