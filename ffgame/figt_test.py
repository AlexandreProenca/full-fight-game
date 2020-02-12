# coding=utf-8
import random


class Bcolors:
    HEADER = '\033[95m'.encode()
    OKBLUE = '\033[94m'.encode()
    OKGREEN = '\033[92m'.encode()
    WARNING = '\033[93m'.encode()
    FAIL = '\033[91m'.encode()
    ENDC = '\033[0m'.encode()
    BOLD = '\033[1m'.encode()
    UNDERLINE = '\033[4m'.encode()


class P(object):

    def __init__(self, name):
        self.name = name
        self.hp = 0
        self.pdef = 0
        self.patk = 0
        self.agility = 0
        self.rage = 0
        self.ready = False

    def hit(self, patk, name, crit=None):
        if crit:
            power = ((patk * crit) - self.pdef)
            self.hp = (self.hp - power)
            print(Bcolors.ENDC + "{} "'\033[93m'" >-----> "'\033[0m'"{} <"'\033[95m'"(-{}) "'\033[0m'"critical>".format(name,self.name, power) + Bcolors.ENDC)
        else:
            power = (patk - self.pdef)
            self.hp = (self.hp - power)
            print(Bcolors.ENDC+"{} "'\033[92m'" >-----> "'\033[0m'"{} <"'\033[91m'"(-{}) "'\033[0m'"hit>".format(name, self.name, power) +Bcolors.ENDC)

    def status(self):
        return "{}({}):HP {}".format(self.name, self.hp, (self.hp * '#'))

    def is_dead(self):
        return self.hp <= 0


p1 = P("Xande")
p1.patk = 20 # determina a força do golpe
p1.pdef = 15 # determina a resistencia fisica ao golpe
p1.hp = 110 # Representa a quantidade de vida
p1.agility = 5 # Determina a agilidade do jogador para escapar dos golpes
p1.rage = 3 # determina a raiva do jogador para acertar golpes fatais


p2 = P("Marcos")
p2.patk = 32
p2.pdef = 1
p2.hp = 100
p1.agility = 10
p2.rage = 5


def chance(probability):
    return random.randrange(100) < probability


def critical(probability):
    return random.randrange(100) < probability


def hit_pvp(p1, p2):
    if chance(90 - p1.agility):
        if critical(10 + p2.rage):
            p1.hit(p2.patk, p2.name, 3)
            if p1.is_dead():
                print(Bcolors.FAIL + "VENCEDOR: {} HP:({})".format(p2.name, p2.hp) +Bcolors.ENDC)
                return True
        else:
            p1.hit(p2.patk, p2.name)
            if p1.is_dead():
                print(Bcolors.FAIL + "VENCEDOR: {} HP:({})".format(p2.name, p2.hp) + Bcolors.ENDC)
                return True
    else:
        print(Bcolors.FAIL + "{} ERRRRRROOOUUU!!!".format(p2.name) + Bcolors.ENDC)




print("********************************************** INICIO *********************************************")
print Bcolors.OKBLUE + p1.status()
print Bcolors.OKGREEN + p2.status() + Bcolors.ENDC

for i in range(1, 100):
    next = raw_input()
    if next == 'n':
        print("********************************************* Jogada {} *********************************************".format(i))
        players = [p1, p2]
        if hit_pvp(p2, p1): break
        if hit_pvp(p1, p2): break
        print(100 * "*")
        print Bcolors.OKBLUE + p1.status()
        print Bcolors.OKGREEN + p2.status() + Bcolors.ENDC




