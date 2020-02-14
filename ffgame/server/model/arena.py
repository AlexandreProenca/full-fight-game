import logging


class Arena:
    players = {}

    @classmethod
    def add_user(cls, username, socket, char):
        cls.players[username] = {'conn': socket, 'char': char}
        logging.info(f"Player Login: {username}")
        print(f"Connected Users {len(Arena.players)} Last Player: {username}")
        return True

    @classmethod
    def close_conn(cls, username):
        char = cls.players.get(username)
        if char:
            char['conn'].close()
            del cls.players[username]

    @classmethod
    def get_user(cls, username):
        return cls.players[username]

    @classmethod
    def del_user(cls, username):
        del cls.players[username]
