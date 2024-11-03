class Spell:
    def __init__(self, name, description, mana_cost, effect_function, rarity="common"):
        self.name = name
        self.description = description
        self.mana_cost = mana_cost
        self.effect_function = effect_function
        self.rarity = rarity

    def cast(self, bot, message, caster, target):
        if caster.mana >= self.mana_cost:
            caster.mana -= self.mana_cost
            self.effect_function(bot, message, caster, target)
        else:
            bot.send_message(message.chat.id, f"Недостаточно маны для использования {self.name}.")

# Примеры эффектов заклинаний
def fireball_effect(bot, message, caster, target):
    damage = 30
    target.take_damage(damage)
    bot.send_message(message.chat.id, f"{target.name} получает {damage} урона от Огненного шара!")

def heal_effect(bot, message, caster, target):
    heal_amount = 20
    target.health += heal_amount
    bot.send_message(message.chat.id, f"{target.name} исцелен на {heal_amount} здоровья!")

def lightning_bolt_effect(bot, message, caster, target):
    damage = 40
    target.take_damage(damage)
    bot.send_message(message.chat.id, f"{target.name} поражён молнией и получает {damage} урона!")

def ice_blast_effect(bot, message, caster, target):
    damage = 25
    target.take_damage(damage)
    bot.send_message(message.chat.id, f"{target.name} получает {damage} урона от ледяного взрыва!")

def shield_effect(bot, message, caster, target):
    shield_amount = 20
    caster.defense += shield_amount
    bot.send_message(message.chat.id, f"{caster.name} получает щит, увеличивая защиту на {shield_amount} на короткое время!")

def poison_effect(bot, message, caster, target):
    damage = 15
    target.take_damage(damage)
    bot.send_message(message.chat.id, f"{target.name} получает {damage} урона от яда!")

def wind_blast_effect(bot, message, caster, target):
    damage = 20
    target.take_damage(damage)
    bot.send_message(message.chat.id, f"{target.name} получает {damage} урона от воздушного взрыва!")

def earth_shake_effect(bot, message, caster, target):
    damage = 35
    target.take_damage(damage)
    bot.send_message(message.chat.id, f"{target.name} получает {damage} урона от землетрясения!")

def dark_magic_effect(bot, message, caster, target):
    damage = 50
    target.take_damage(damage)
    bot.send_message(message.chat.id, f"{target.name} получает {damage} урона от тёмной магии!")

def holy_light_effect(bot, message, caster, target):
    heal_amount = 50
    target.health += heal_amount
    bot.send_message(message.chat.id, f"{target.name} исцелен на {heal_amount} здоровья Священным Светом!")

# Список заклинаний
spells = [
    # Обычные заклинания
    Spell(name="Огненный шар", description="Атакующее заклинание, наносящее огненный урон.", mana_cost=10, effect_function=fireball_effect, rarity="common"),
    Spell(name="Исцеление", description="Восстанавливает здоровье цели.", mana_cost=8, effect_function=heal_effect, rarity="common"),
    Spell(name="Ледяной взрыв", description="Атакующее заклинание, наносящее ледяной урон.", mana_cost=12, effect_function=ice_blast_effect, rarity="common"),
    Spell(name="Ядовитый удар", description="Атакующее заклинание, наносящее урон ядом.", mana_cost=10, effect_function=poison_effect, rarity="common"),
    Spell(name="Воздушный взрыв", description="Атакующее заклинание, наносящее урон воздухом.", mana_cost=10, effect_function=wind_blast_effect, rarity="common"),
    Spell(name="Землетрясение", description="Атакующее заклинание, наносящее урон землей.", mana_cost=15, effect_function=earth_shake_effect, rarity="common"),
    Spell(name="Молния", description="Атакующее заклинание, наносящее электрический урон.", mana_cost=15, effect_function=lightning_bolt_effect, rarity="common"),
    Spell(name="Щит", description="Создаёт щит, увеличивающий защиту цели.", mana_cost=10, effect_function=shield_effect, rarity="common"),
    Spell(name="Темная магия", description="Атакующее заклинание, наносящее урон тёмной магией.", mana_cost=20, effect_function=dark_magic_effect, rarity="common"),
    Spell(name="Священный свет", description="Лечит цель с помощью Священного Света.", mana_cost=20, effect_function=holy_light_effect, rarity="common"),

    # Необычные заклинания
    Spell(name="Огненный шторм", description="Мощное атакующее заклинание, наносящее огненный урон всем врагам.", mana_cost=20, effect_function=fireball_effect, rarity="uncommon"),
    Spell(name="Ледяной барьер", description="Создаёт барьер изо льда, увеличивающий защиту цели.", mana_cost=12, effect_function=shield_effect, rarity="uncommon"),
    Spell(name="Вихрь", description="Атакующее заклинание, наносящее урон магическим вихрем.", mana_cost=18, effect_function=wind_blast_effect, rarity="uncommon"),
    Spell(name="Отравление", description="Атакующее заклинание, наносящее урон ядом.", mana_cost=15, effect_function=poison_effect, rarity="uncommon"),
    Spell(name="Цепная молния", description="Атакующее заклинание, поражающее несколько целей.", mana_cost=25, effect_function=lightning_bolt_effect, rarity="uncommon"),
    Spell(name="Большое исцеление", description="Восстанавливает большое количество здоровья цели.", mana_cost=20, effect_function=heal_effect, rarity="uncommon"),
    Spell(name="Снежная буря", description="Мощное атакующее заклинание, наносящее ледяной урон всем врагам.", mana_cost=30, effect_function=ice_blast_effect, rarity="uncommon"),
    Spell(name="Каменная стена", description="Создаёт защитную стену из камня.", mana_cost=25, effect_function=shield_effect, rarity="uncommon"),
    Spell(name="Взрывная волна", description="Наносит урон всем врагам вокруг цели.", mana_cost=22, effect_function=earth_shake_effect, rarity="uncommon"),
    Spell(name="Световой барьер", description="Создаёт барьер, поглощающий урон.", mana_cost=20, effect_function=shield_effect, rarity="uncommon"),

    # Редкие заклинания
    Spell(name="Огненный вихрь", description="Создаёт вихрь огня, наносящий урон всем врагам.", mana_cost=35, effect_function=fireball_effect, rarity="rare"),
    Spell(name="Грозовой шторм", description="Вызывает грозу, наносящую урон всем врагам.", mana_cost=40, effect_function=lightning_bolt_effect, rarity="rare"),
    Spell(name="Ледяное поле", description="Создаёт ледяное поле, наносящее урон и замедляющее врагов.", mana_cost=35, effect_function=ice_blast_effect, rarity="rare"),
    Spell(name="Землетрясение", description="Вызывает сильное землетрясение, наносящее урон всем врагам.", mana_cost=50, effect_function=earth_shake_effect, rarity="rare"),
    Spell(name="Торнадо", description="Создаёт торнадо, наносящее урон и отбрасывающее врагов.", mana_cost=45, effect_function=wind_blast_effect, rarity="rare"),
    Spell(name="Кислотный дождь", description="Вызывает кислотный дождь, наносящий урон всем врагам.", mana_cost=40, effect_function=poison_effect, rarity="rare"),
    Spell(name="Проклятие", description="Накладывает проклятие на цель, снижая её характеристики.", mana_cost=30, effect_function=dark_magic_effect, rarity="rare"),
    Spell(name="Божественное исцеление", description="Мощное исцеляющее заклинание, восстанавливающее большое количество здоровья.", mana_cost=35, effect_function=holy_light_effect, rarity="rare"),
    Spell(name="Светлый вихрь", description="Создаёт вихрь света, наносящий урон всем врагам.", mana_cost=35, effect_function=holy_light_effect,    rarity="rare"),

    # Эпические заклинания
    Spell(name="Метеоритный дождь", description="Вызывает падение метеоритов, наносящих огромный урон всем врагам.", mana_cost=50, effect_function=fireball_effect, rarity="epic"),
    Spell(name="Громовой удар", description="Мощное заклинание, наносящее огромный электрический урон одной цели.", mana_cost=45, effect_function=lightning_bolt_effect, rarity="epic"),
    Spell(name="Магический барьер", description="Создаёт мощный барьер, защищающий от атак.", mana_cost=40, effect_function=shield_effect, rarity="epic"),
    Spell(name="Огненная буря", description="Создаёт бурю огня, наносящую урон всем врагам.", mana_cost=50, effect_function=fireball_effect, rarity="epic"),
    Spell(name="Ледяной дракон", description="Призывает ледяного дракона, наносящего огромный урон врагам.", mana_cost=50, effect_function=ice_blast_effect, rarity="epic"),
    Spell(name="Астральный удар", description="Атакующее заклинание, наносящее урон астральной энергией.", mana_cost=45, effect_function=dark_magic_effect, rarity="epic"),
    Spell(name="Священная аура", description="Создаёт ауру, исцеляющую всех союзников.", mana_cost=40, effect_function=holy_light_effect, rarity="epic"),
    Spell(name="Магическое исцеление", description="Мощное заклинание, восстанавливающее много здоровья цели.", mana_cost=45, effect_function=heal_effect, rarity="epic"),
    Spell(name="Гиперскорость", description="Повышает скорость и ловкость цели.", mana_cost=35, effect_function=shield_effect, rarity="epic"),
    Spell(name="Призрачный удар", description="Атакует врага призрачной силой, нанося большой урон.", mana_cost=40, effect_function=dark_magic_effect, rarity="epic"),

    # Легендарные заклинания
    Spell(name="Воскрешение", description="Воскрешает павшего союзника.", mana_cost=50, effect_function=heal_effect, rarity="legendary"),
    Spell(name="Армагеддон", description="Вызывает разрушительное заклинание, наносящее огромный урон всем врагам.", mana_cost=60, effect_function=fireball_effect, rarity="legendary"),
    Spell(name="Кристальный голем", description="Призывает кристального голема для защиты и атаки.", mana_cost=55, effect_function=shield_effect, rarity="legendary"),
    Spell(name="Огненный дракон", description="Призывает огненного дракона, наносящего огромный урон врагам.", mana_cost=60, effect_function=fireball_effect, rarity="legendary"),
    Spell(name="Тёмная буря", description="Создаёт бурю тьмы, наносящую огромный урон всем врагам.", mana_cost=55, effect_function=dark_magic_effect, rarity="legendary"),
    Spell(name="Священный суд", description="Наносит огромный урон одной цели с помощью священной силы.", mana_cost=55, effect_function=holy_light_effect, rarity="legendary"),
    Spell(name="Призыв элементалей", description="Призывает элементалей для атаки врагов.", mana_cost=60, effect_function=fireball_effect, rarity="legendary"),
    Spell(name="Божественная защита", description="Создаёт мощную защиту для всех союзников.", mana_cost=55, effect_function=shield_effect, rarity="legendary"),
    Spell(name="Магическое поле", description="Создаёт магическое поле, наносящее урон и защищающее союзников.", mana_cost=60, effect_function=dark_magic_effect, rarity="legendary"),
    Spell(name="Светлый дракон", description="Призывает светлого дракона, наносящего огромный урон врагам.", mana_cost=60, effect_function=holy_light_effect, rarity="legendary"),
]
