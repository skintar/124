class Enemy:
    def __init__(self, name, health, damage, defense, abilities=None, rarity="common"):
        self.name = name
        self.health = health
        self.damage = damage
        self.defense = defense
        self.abilities = abilities if abilities else []
        self.rarity = rarity

    def take_damage(self, amount):
        damage_taken = max(0, amount - self.defense)
        self.health = max(0, self.health - damage_taken)
        return damage_taken

    def is_alive(self):
        return self.health > 0

# Обычные враги
goblin = Enemy(name="Гоблин", health=30, damage=5, defense=2, rarity="common")
skeleton = Enemy(name="Скелет", health=35, damage=7, defense=3, rarity="common")
bandit = Enemy(name="Бандит", health=40, damage=6, defense=2, rarity="common")
wolf = Enemy(name="Волк", health=25, damage=4, defense=1, rarity="common")
zombie = Enemy(name="Зомби", health=50, damage=5, defense=1, rarity="common")
rat = Enemy(name="Крыса", health=15, damage=3, defense=1, rarity="common")
bat = Enemy(name="Летучая мышь", health=20, damage=4, defense=1, rarity="common")
spider = Enemy(name="Паук", health=25, damage=5, defense=2, rarity="common")
snake = Enemy(name="Змея", health=20, damage=6, defense=1, rarity="common")
imp = Enemy(name="Имп", health=30, damage=6, defense=2, rarity="common")

# Необычные враги
orc = Enemy(name="Орк", health=50, damage=10, defense=4, rarity="uncommon")
troll = Enemy(name="Тролль", health=60, damage=8, defense=5, abilities=["Регенерация"], rarity="uncommon")
ogre = Enemy(name="Огр", health=80, damage=12, defense=5, rarity="uncommon")
harpy = Enemy(name="Гарпия", health=45, damage=6, defense=3, abilities=["Летать"], rarity="uncommon")
wraith = Enemy(name="Призрак", health=40, damage=10, defense=2, abilities=["Неосязаемость"], rarity="uncommon")
gnoll = Enemy(name="Гнолл", health=55, damage=9, defense=3, rarity="uncommon")
mermaid = Enemy(name="Русалка", health=50, damage=7, defense=4, abilities=["Очарование"], rarity="uncommon")
centaur = Enemy(name="Кентавр", health=70, damage=11, defense=5, rarity="uncommon")
dryad = Enemy(name="Дриада", health=45, damage=8, defense=3, abilities=["Лесная магия"], rarity="uncommon")
mimic = Enemy(name="Мимик", health=60, damage=10, defense=4, abilities=["Маскировка"], rarity="uncommon")

# Редкие враги
vampire = Enemy(name="Вампир", health=70, damage=12, defense=6, abilities=["Лечение кровью"], rarity="rare")
lich = Enemy(name="Лич", health=80, damage=15, defense=5, abilities=["Магия тьмы"], rarity="rare")
minotaur = Enemy(name="Минотавр", health=90, damage=18, defense=7, rarity="rare")
basilisk = Enemy(name="Базилиск", health=60, damage=14, defense=6, abilities=["Паралич"], rarity="rare")
golem = Enemy(name="Голем", health=100, damage=10, defense=10, abilities=["Каменная кожа"], rarity="rare")
werewolf = Enemy(name="Оборотень", health=85, damage=16, defense=5, abilities=["Превращение"], rarity="rare")
sphinx = Enemy(name="Сфинкс", health=75, damage=13, defense=6, abilities=["Загадки"], rarity="rare")
chimera = Enemy(name="Химера", health=95, damage=17, defense=8, abilities=["Огненное дыхание"], rarity="rare")
medusa = Enemy(name="Медуза", health=70, damage=11, defense=5, abilities=["Паралич взгляда"], rarity="rare")
griffin = Enemy(name="Грифон", health=90, damage=14, defense=7, abilities=["Полёт"], rarity="rare")

# Эпические враги
dragon = Enemy(name="Дракон", health=150, damage=20, defense=10, abilities=["Огненное дыхание", "Полёт"], rarity="epic")
demon_lord = Enemy(name="Демон-лорд", health=200, damage=25, defense=12, abilities=["Тьма", "Адское пламя"], rarity="epic")
kraken = Enemy(name="Кракен", health=180, damage=22, defense=8, abilities=["Удушение"], rarity="epic")
hydra = Enemy(name="Гидра", health=160, damage=19, defense=9, abilities=["Множество голов"], rarity="epic")
phoenix = Enemy(name="Феникс", health=250, damage=18, defense=10, abilities=["Возрождение", "Огненные крылья"], rarity="epic")
behemoth = Enemy(name="Бегемот", health=200, damage=23, defense=11, abilities=["Сейсмический удар"], rarity="epic")
leviathan = Enemy(name="Левиафан", health=220, damage=24, defense=12, abilities=["Цунами"], rarity="epic")
titan = Enemy(name="Титан", health=240, damage=26, defense=13, abilities=["Титаническая сила"], rarity="epic")
shadow_reaper = Enemy(name="Жнец теней", health=280, damage=32, defense=13, abilities=["Поглощение душ"], rarity="epic")
celestial_dragon = Enemy(name="Небесный дракон", health=500, damage=40, defense=25, abilities=["Божественный огонь", "Полёт"], rarity="epic")

# Легендарные враги
ancient_behemoth = Enemy(name="Древний Бегемот", health=300, damage=30, defense=15, abilities=["Сейсмический удар", "Неуязвимость"], rarity="legendary")
elder_lich = Enemy(name="Древний Лич", health=300, damage=35, defense=15, abilities=["Некромантия"], rarity="legendary")
dark_phoenix = Enemy(name="Тёмный Феникс", health=350, damage=30, defense=20, abilities=["Тёмное возрождение"], rarity="legendary")
fire_giant = Enemy(name="Огненный Великан", health=400, damage=38, defense=18, abilities=["Огненные удары"], rarity="legendary")
storm_titan = Enemy(name="Титан Шторма", health=450, damage=42, defense=22, abilities=["Молнии"], rarity="legendary")
death_knight = Enemy(name="Рыцарь Смерти", health=320, damage=36, defense=17, abilities=["Некромантия"], rarity="legendary")
nightmare = Enemy(name="Кошмар", health=300, damage=35, defense=12, abilities=["Иллюзии"], rarity="legendary")
void_walker = Enemy(name="Путешественник Пустоты", health=350, damage=28, defense=16, abilities=["Телепортация"], rarity="legendary")
archangel = Enemy(name="Архангел", health=400, damage=40, defense=20, abilities=["Священный свет"], rarity="legendary")
abyssal_horror = Enemy(name="Ужас из Бездны", health=450, damage=45, defense=25, abilities=["Поглощение душ"], rarity="legendary")

# Список всех врагов
enemies = [
    goblin, skeleton, bandit, wolf, zombie, rat, bat, spider, snake, imp,
    orc, troll, ogre, harpy, wraith, gnoll, mermaid, centaur, dryad, mimic,
    vampire, lich, minotaur, basilisk, golem, werewolf, sphinx, chimera, medusa, griffin,
    dragon, demon_lord, kraken, hydra, phoenix, behemoth, leviathan, titan, shadow_reaper, celestial_dragon,
    ancient_behemoth, elder_lich, dark_phoenix, fire_giant, storm_titan, death_knight, nightmare, void_walker, archangel, abyssal_horror
]