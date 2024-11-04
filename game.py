from player import Player
from enemies import Enemy
from locations import Location
from npc import NPC

class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.locations = []
        self.npcs = []

    def start(self):
        print("Game started")
        # Initialize game world
