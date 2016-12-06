# -*- coding: utf-8 -*-
"""
Classe para lidar com as conexoes dos clientes
"""
import SocketServer as socketServer
import time
import json
import logging
import player_handler


def agora():
    return time.ctime(time.time())


class LidaComCliente(socketServer.BaseRequestHandler):

    def handle(self):
        # Para cada conexão com cliente nós:
        # Imprimimos a identificação do cliente e o tempo
        print(self.client_address, agora())
        print(dir(self))

        while True:
            # Recebe data do cliente
            infodata = self.request.recv(1024)
            if not infodata:
                self.request.send("Treta no infodata: {}".format(infodata))
            self.router_message(infodata)

    def router_message(self, message):
        parsed = None
        try:
            parsed = json.loads(message)
        except Exception, e:
            logging.info("Exception: {} Message {}".format(e, message))

        if parsed:
            if parsed['type'] == 'authenticate':
                if parsed['payload']['user']:
                    player_handler.login(parsed['payload']['user'])
                    self.request.send("Login OK")
                else:
                    if parsed['payload']['logout']:
                        player_handler.logout(parsed['payload']['user'])
                        self.request.send("Logout OK")
