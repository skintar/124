class Item:
    def __init__(self, name, description, effect_function=None, rarity="common"):
        self.name = name
        self.description = description
        self.effect_function = effect_function
        self.rarity = rarity

    def use(self, bot, message, entity):
        if self.effect_function:
            self.effect_function(bot, message, entity)
        else:
            bot.send_message(message.chat.id, f"{self.name} не имеет эффекта для использования.")

# Описание и эффекты предметов
def heal_effect(bot, message, entity):
    heal_amount = 20
    entity.health += heal_amount
    bot.send_message(message.chat.id, f"{entity.name} исцелен на {heal_amount} здоровья!")

def fireball_effect(bot, message, entity):
    fireball_damage = 30
    entity.take_damage(fireball_damage)
    bot.send_message(message.chat.id, f"{entity.name} получает {fireball_damage} урона от огненного шара!")

def antidote_effect(bot, message, entity):
    entity.status_effects.clear()
    bot.send_message(message.chat.id, f"{entity.name} избавляется от всех негативных эффектов!")

def strength_potion_effect(bot, message, entity):
    entity.strength += 5
    bot.send_message(message.chat.id, f"{entity.name} выпил зелье силы и его сила увеличилась на 5!")

def defense_potion_effect(bot, message, entity):
    entity.defense += 5
    bot.send_message(message.chat.id, f"{entity.name} выпил зелье защиты и его защита увеличилась на 5!")

def agility_potion_effect(bot, message, entity):
    entity.agility += 5
    bot.send_message(message.chat.id, f"{entity.name} выпил зелье ловкости и его ловкость увеличилась на 5!")

# Примеры предметов
healing_potion = Item(
    name="Зелье исцеления",
    description="Маленький флакон с жидкостью, восстанавливающий здоровье.",
    effect_function=heal_effect,
    rarity="common"
)

fire_bomb = Item(
    name="Огненная бомба",
    description="Взрывоопасное устройство, наносящее урон огнем.",
    effect_function=fireball_effect,
    rarity="rare"
)

antidote = Item(
    name="Антидот",
    description="Средство для снятия всех негативных эффектов.",
    effect_function=antidote_effect,
    rarity="common"
)

strength_potion = Item(
    name="Зелье силы",
    description="Зелье, временно увеличивающее силу.",
    effect_function=strength_potion_effect,
    rarity="uncommon"
)

defense_potion = Item(
    name="Зелье защиты",
    description="Зелье, временно увеличивающее защиту.",
    effect_function=defense_potion_effect,
    rarity="uncommon"
)

agility_potion = Item(
    name="Зелье ловкости",
    description="Зелье, временно увеличивающее ловкость.",
    effect_function=agility_potion_effect,
    rarity="uncommon"
)

# Создание большого количества предметов
items = [
    healing_potion,
    fire_bomb,
    antidote,
    strength_potion,
    defense_potion,
    agility_potion,
]

# Генерация дополнительных предметов
for i in range(1, 196):
    items.append(Item(
        name=f"Особый предмет {i}",
        description=f"Это особый предмет номер {i}.",
        rarity="rare" if i % 10 == 0 else "common"
    ))
