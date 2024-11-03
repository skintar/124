import random
from telebot import types

class StatusEffect:
    def __init__(self, name, duration, effect_function):
        self.name = name
        self.duration = duration
        self.effect_function = effect_function

    def apply(self, bot, message, entity):
        self.effect_function(bot, message, entity)
        self.duration -= 1

class Ability:
    def __init__(self, name, effect_function, cooldown=0):
        self.name = name
        self.effect_function = effect_function
        self.cooldown = cooldown
        self.current_cooldown = 0

    def use(self, bot, message, caster, target):
        if self.current_cooldown == 0:
            self.effect_function(bot, message, caster, target)
            self.current_cooldown = self.cooldown

    def tick_cooldown(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

class Item:
    def __init__(self, name, effect_function, rarity="common"):
        self.name = name
        self.effect_function = effect_function
        self.rarity = rarity

    def use(self, bot, message, entity):
        self.effect_function(bot, message, entity)

class Weapon:
    def __init__(self, name, damage, damage_type="physical"):
        self.name = name
        self.damage = damage
        self.damage_type = damage_type

class Armor:
    def __init__(self, name, defense, resistance=None):
        self.name = name
        self.defense = defense
        self.resistance = resistance or []

class Equipment:
    def __init__(self):
        self.weapon = None
        self.armor = None

    def equip_weapon(self, weapon):
        self.weapon = weapon

    def equip_armor(self, armor):
        self.armor = armor

class Entity:
    def __init__(self, name, health, damage, defense, agility, level=1, abilities=None, inventory=None, weaknesses=None, resistances=None):
        self.name = name
        self.health = health
        self.damage = damage
        self.defense = defense
        self.agility = agility
        self.level = level
        self.abilities = abilities or []
        self.status_effects = []
        self.gold = 0
        self.experience = 0
        self.inventory = inventory or []
        self.weaknesses = weaknesses or []
        self.resistances = resistances or []
        self.equipment = Equipment()
        self.kills = {"rat": 0, "goblin": 0, "dragon": 0, "zombie": 0, "ice_golem": 0, "vampire": 0}

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage, damage_type=None):
        if damage_type in self.resistances:
            damage *= 0.5
        if damage_type in self.weaknesses:
            damage *= 1.5
        if self.equipment.armor and damage_type in self.equipment.armor.resistance:
            damage *= 0.5
        damage_taken = max(0, damage - self.defense - (self.equipment.armor.defense if self.equipment.armor else 0))
        self.health -= damage_taken
        return damage_taken

    def add_status_effect(self, effect):
        self.status_effects.append(effect)

    def handle_status_effects(self, bot, message):
        for effect in self.status_effects[:]:
            effect.apply(bot, message, self)
            if effect.duration <= 0:
                self.status_effects.remove(effect)

    def use_ability(self, bot, message, target):
        available_abilities = [ability for ability in self.abilities if ability.current_cooldown == 0]
        if available_abilities:
            ability = random.choice(available_abilities)
            bot.send_message(message.chat.id, f"{self.name} использует {ability.name}!")
            ability.use(bot, message, self, target)

    def tick_abilities(self):
        for ability in self.abilities:
            ability.tick_cooldown()

    def use_item(self, bot, message, item_name):
        for item in self.inventory:
            if item.name == item_name:
                item.use(bot, message, self)
                self.inventory.remove(item)
                bot.send_message(message.chat.id, f"{self.name} использует {item.name}.")
                return

class Quest:
    def init(self, name, description, goal, reward):
        self.name = name
        self.description = description
        self.goal = goal
        self.reward = reward
        self.completed = False

    def check_completion(self, player):
        if self.goal(player):
            self.completed = True
            player.gold += self.reward['gold']
            player.experience += self.reward['experience']
            return True
        return False

def create_quests():
    quests = [
        Quest("Убить 10 крыс", "Избавь деревню от 10 крыс", lambda player: player.kills['rat'] >= 10, {"gold": 50, "experience": 100}),
        Quest("Победить дракона", "Победи дракона, угрожающего королевству", lambda player: player.kills['dragon'] >= 1, {"gold": 500, "experience": 500})
    ]
    return quests

def poison_effect(bot, message, caster, target):
    bot.send_message(message.chat.id, f"{target.name} отравлен и теряет 5 здоровья!")
    target.take_damage(5)

def heal_effect(bot, message, caster, target):
    heal_amount = 20
    target.health += heal_amount
    bot.send_message(message.chat.id, f"{target.name} исцелен на {heal_amount} здоровья!")

def fireball_effect(bot, message, caster, target):
    fireball_damage = 30
    damage_dealt = target.take_damage(fireball_damage, damage_type="fire")
    bot.send_message(message.chat.id, f"{target.name} получает {damage_dealt} урона от огненного шара!")

def shield_effect(bot, message, caster, target):
    caster.defense += 5
    bot.send_message(message.chat.id, f"{caster.name} повышает свою защиту на 5!")

def stun_effect(bot, message, caster, target):
    target.add_status_effect(StatusEffect("Оглушение", 1, lambda bot, message, entity: bot.send_message(message.chat.id, f"{entity.name} оглушен и пропускает ход!")))

def freeze_effect(bot, message, caster, target):
    target.add_status_effect(StatusEffect("Заморозка", 2, lambda bot, message, entity: bot.send_message(message.chat.id, f"{entity.name} заморожен и не может двигаться!")))

def level_up(bot, message, player):
    player.level += 1
    player.health += 10
    player.damage += 2
    player.defense += 1
    player.agility += 1
    bot.send_message(message.chat.id, f"Поздравляем! Вы повысили уровень до {player.level}. Ваши характеристики улучшены!")

def check_experience(bot, message, player):
    experience_needed = player.level * 50
    if player.experience >= experience_needed:
        player.experience -= experience_needed
        level_up(bot, message, player)

def player_turn(bot, message, player, enemy):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    button_attack = types.KeyboardButton('Атаковать')
    button_ability = types.KeyboardButton('Использовать способность')
    button_item = types.KeyboardButton('Использовать предмет')
    button_defend = types.KeyboardButton('Защищаться')
    markup.add(button_attack, button_ability, button_item, button_defend)
    bot.send_message(message.chat.id, "Ваш ход! Выберите действие:", reply_markup=markup)

    @bot.message_handler(func=lambda msg: msg.text in ['Атаковать', 'Использовать способность', 'Использовать предмет', 'Защищаться'])
    def handle_player_action(msg):
        if msg.text == 'Атаковать':
            player_damage = random.randint(player.damage // 2, player.damage * 2)
            damage_dealt = enemy.take_damage(player_damage)
            bot.send_message(msg.chat.id, f"Вы нанесли {damage_dealt} урона {enemy.name}. Осталось здоровья: {enemy.health}")

        elif msg.text == 'Использовать способность':
            abilities_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
            for ability in player.abilities:
                abilities_markup.add(types.KeyboardButton(ability.name))
            bot.send_message(msg.chat.id, "Выберите способность:", reply_markup=abilities_markup)

            @bot.message_handler(func=lambda msg: any(ability.name == msg.text for ability in player.abilities))
            def handle_ability_choice(msg):
                for ability in player.abilities:
                    if msg.text == ability.name and ability.current_cooldown == 0:
                        ability.use(bot, msg, player, enemy)
                        player.tick_abilities()
                        bot.send_message(msg.chat.id, f"Вы использовали {ability.name}.")
                        break

        elif msg.text == 'Использовать предмет':
            items_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
            for item in player.inventory:
                items_markup.add(types.KeyboardButton(item.name))
            bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=items_markup)

            @bot.message_handler(func=lambda msg: any(item.name == msg.text for item in player.inventory))
            def handle_item_choice(msg):
                player.use_item(bot, msg, msg.text)

        elif msg.text == 'Защищаться':
            player.defense += 5
            bot.send_message(msg.chat.id, f"{player.name} повышает свою защиту на 5!")

        # Переход хода к врагу
        if enemy.is_alive():
            enemy_turn(bot, msg, player, enemy)
        else:
            player.kills[enemy.name.lower()] += 1
            check_experience(bot, msg, player)
            bot.send_message(msg.chat.id, f"Вы победили {enemy.name}!")

def enemy_turn(bot, message, player, enemy):
    if random.random() < enemy.agility * 0.01:
        bot.send_message(message.chat.id, f"{enemy.name} уклонился от вашей атаки!")
    else:
        damage_dealt = player.take_damage(enemy.damage)
        bot.send_message(message.chat.id, f"{enemy.name} атакует вас, нанося {damage_dealt} урона. Ваше здоровье: {player.health}")

        # Если у врага есть способности, он может их использовать
        if enemy.abilities and random.random() < 0.5:  # 50% шанс на использование способности
            enemy.use_ability(bot, message, player)

    if player.is_alive():
        player_turn(bot, message, player, enemy)
    else:
        bot.send_message(message.chat.id, "Вы проиграли бой!")

def fight(bot, message, player, enemy):
    while player.is_alive() and enemy.is_alive():
        player.handle_status_effects(bot, message)
        enemy.handle_status_effects(bot, message)

        player_turn(bot, message, player, enemy)

        player.tick_abilities()
        enemy.tick_abilities()

    if not player.is_alive():
        bot.send_message(message.chat.id, "Вы проиграли бой!")
    else:
        bot.send_message(message.chat.id, f"Вы победили {enemy.name}!")
        player.gold += enemy.gold
        player.experience += enemy.experience
        check_experience(bot, message, player)

def create_player():
    abilities = [
        Ability("Исцеление", heal_effect, cooldown=3),
        Ability("Огненный шар", fireball_effect, cooldown=5),
        Ability("Щит", shield_effect, cooldown=4),
        Ability("Оглушение", stun_effect, cooldown=4),
        Ability("Заморозка", freeze_effect, cooldown=5)
    ]
    inventory = [
        Item("Зелье исцеления", heal_effect, rarity="common"),
        Item("Огненная бомба", fireball_effect, rarity="rare"),
        Item("Антидот", lambda bot, message, entity: entity.status_effects.clear(), rarity="common")
    ]
    player = Entity("Игрок", health=100, damage=20, defense=5, agility=10, level=1, abilities=abilities, inventory=inventory)
    player.equipment.equip_weapon(Weapon("Меч", 10))
    player.equipment.equip_armor(Armor("Кожаная броня", 3, resistance=["physical"]))
    return player

def create_rat():
    abilities = [Ability("Отравляющий укус", poison_effect, cooldown=2)]
    return Entity("Крыса", health=30, damage=5, defense=1, agility=5, abilities=abilities, weaknesses=["fire"])

def create_goblin():
    abilities = [Ability("Щит", shield_effect, cooldown=3)]
    return Entity("Гоблин", health=40, damage=7, defense=2, agility=6, abilities=abilities, resistances=["fire"], weaknesses=["ice"])

def create_dragon():
    abilities = [
        Ability("Огненное дыхание", fireball_effect, cooldown=3),
        Ability("Исцеление", heal_effect, cooldown=5)
    ]
    return Entity("Дракон", health=200, damage=20, defense=10, agility=5, abilities=abilities, resistances=["fire"], weaknesses=["ice"])

def create_zombie():
    abilities = [Ability("Укус", poison_effect, cooldown=4)]
    return Entity("Зомби", health=50, damage=10, defense=3, agility=2, abilities=abilities, resistances=["poison"], weaknesses=["fire"])

def create_ice_golem():
    abilities = [Ability("Заморозка", freeze_effect, cooldown=3)]
    return Entity("Ледяной голем", health=100, damage=15, defense=10, agility=1, abilities=abilities, resistances=["ice"], weaknesses=["fire"])

def create_vampire():
    abilities = [Ability("Иссушение", lambda bot, message, caster, target: target.take_damage(10) and caster.health += 10, cooldown=4)]
    return Entity("Вампир", health=80, damage=12, defense=5, agility=8, abilities=abilities, weaknesses=["holy"])

def create_enemy(enemy_type):
    if enemy_type == "rat":
        return create_rat()
    elif enemy_type == "goblin":
        return create_goblin()
    elif enemy_type == "dragon":
        return create_dragon()
    elif enemy_type == "zombie":
        return create_zombie()
    elif enemy_type == "ice_golem":
        return create_ice_golem()
    elif enemy_type == "vampire":
        return create_vampire()
    else:
        raise ValueError(f"Unknown enemy type: {enemy_type}")

def start_fight(bot, message, enemy_type):
    player = create_player()
    enemy = create_enemy(enemy_type)
    fight(bot, message, player, enemy)

# Пример использования:
# start_fight(bot, message, "goblin")