from item import Item

class Weapon(Item):

    def __init__(self):
        super(Item, self).__init__()
        self.name = name
        self.equipped = False

    def equip(self):
        self.equipped = True

    def unnequip(self):
        self.equipped = False
        
