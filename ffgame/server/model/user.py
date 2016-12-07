#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Class to mantein a dict users in mmemory
"""
import logging


class User:

    users = {}

    @classmethod
    def open(cls, email, conn):
        cls.users[email] = conn
        print cls.users
        logging.info('Player Login: {}'.format(email))
        print 'Connected Users (+)'+str(len(User.users))+' Last Player: '+email

    @classmethod
    def close(cls, user):
       pass
