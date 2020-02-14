import random


class Char:
    def __init__(self, username: str):
        self.username = username
        self.name = ''
        self.hp = 0
        self.p_def = 0
        self.p_atk = 0
        self.m_def = 0
        self.m_atk = 0
        self.agility = 0
        self.rage = 0
        self.skill_points = 150

    def f_hit(self) -> int:
        return self.p_atk + (random.randint(1, self.rage))

    def m_speel(self) -> int:
        return self.m_atk + (random.randint(1, self.rage))

    def f_defence(self) -> int:
        return self.p_def

    def m_defence(self) -> int:
        return self.m_def

    def status(self) -> str:
        return f"{self.name}({self.hp}):HP {self.hp * '#'}\n"

    def is_dead(self) -> bool:
        return self.hp <= 0
