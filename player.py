import random

class Player:
    def __init__(self):
        self.name = ''
        self.hp = 100
        self.mp = 50
        self.level = 1
        self.inventory = []
        self.location = None

    def move(self, new_location):
        self.location = new_location
        print(f"{self.name} moved to {self.location.name}")

    def attack(self, target):
        damage = random.randint(1, 10)
        target.hp -= damage
        print(f"{self.name} attacked {target.name} for {damage} damage")

    def cast_spell(self, spell, target):
        if spell.cost > self.mp:
            print("Not enough MP")
        else:
            self.mp -= spell.cost
            spell.effect(target)
            print(f"{self.name} cast {spell.name} on {target.name}")