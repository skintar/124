import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import firebase_admin
from firebase_admin import credentials, firestore
import random
from locations import game_world
from actions import process_action
from npc import *
from items import items
from enemies import enemies
from spells import spells

# Инициализация Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Настройка Telegram Bot API
API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
if not API_TOKEN:
    raise ValueError("Необходимо установить переменную окружения TELEGRAM_API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# Глобальные переменные для хранения данных пользователей и состояний
user_data = {}
user_states = {}

def save_user_data(chat_id, user_data):
    try:
        db.collection('users').document(str(chat_id)).set(user_data)
        print(f"Данные пользователя {chat_id} сохранены в Firebase.")
    except Exception as e:
        print(f"Ошибка при сохранении данных пользователя {chat_id} в Firebase: {e}")

def get_user_data(chat_id):
    try:
        doc_ref = db.collection('users').document(str(chat_id))
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    except Exception as e:
        print(f"Ошибка при получении данных пользователя {chat_id} из Firebase: {e}")
        return None

class Entity:
    def __init__(self, name, race, character_class, profession, health, mana, strength, defense, agility):
        self.name = name
        self.race = race
        self.character_class = character_class
        self.profession = profession
        self.health = health
        self.mana = mana
        self.strength = strength
        self.defense = defense
        self.agility = agility
        self.inventory = []
        self.spells = []

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.health = max(0, self.health - actual_damage)
        return actual_damage

    def is_alive(self):
        return self.health > 0

    def add_item(self, item):
        self.inventory.append(item)

    def add_spell(self, spell):
        self.spells.append(spell)

def give_initial_weapon(user_class):
    weapons = {
        'воин': 'меч',
        'маг': 'посох',
        'вор': 'кинжал',
        'жрец': 'освященный посох'
    }
    return weapons.get(user_class, 'палка')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    create_character_button = InlineKeyboardButton("Создать персонажа", callback_data='create_character')
    markup.add(create_character_button)
    bot.send_message(message.chat.id, "Добро пожаловать в наш мир приключений! Нажмите на кнопку ниже, чтобы начать создание вашего персонажа.", reply_markup=markup)

def request_name(message):
    msg = bot.reply_to(message, "Как зовут вашего героя?")
    bot.register_next_step_handler(msg, set_name)

@bot.callback_query_handler(func=lambda call: call.data == 'create_character')
def create_character(call):
    chat_id = call.message.chat.id
    if get_user_data(chat_id):
        bot.send_message(chat_id, "У вас уже есть персонаж. Используйте /start_quest, чтобы начать приключение.")
        return

    request_name(call.message)

def set_name(message):
    chat_id = message.chat.id
    name = message.text.strip()
    user_states[chat_id] = {'name': name}

    markup = InlineKeyboardMarkup()
    races = ['человек', 'эльф', 'гном', 'орк']
    for race in races:
        markup.add(InlineKeyboardButton(race.capitalize(), callback_data=f"set_race:{race}"))
    bot.send_message(chat_id, f"Вы выбрали имя: {name}. Теперь выберите расу вашего героя:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('set_race:'))
def set_race(call):
    chat_id = call.message.chat.id
    race_choice = call.data.split(':')[1]
    user_states[chat_id]['race'] = race_choice

    markup = InlineKeyboardMarkup()
    classes = ['воин', 'маг', 'вор', 'жрец']
    for cls in classes:
        markup.add(InlineKeyboardButton(cls.capitalize(), callback_data=f"set_class:{cls}"))
    bot.send_message(chat_id, f"Вы выбрали расу: {race_choice}. Теперь выберите класс вашего героя:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('set_class:'))
def set_class(call):
    chat_id = call.message.chat.id
    class_choice = call.data.split(':')[1]
    user_states[chat_id]['class'] = class_choice

    markup = InlineKeyboardMarkup()
    professions = ['кузнец', 'повар', 'ткач']
    for profession in professions:
        markup.add(InlineKeyboardButton(profession.capitalize(), callback_data=f"set_profession:{profession}"))
    bot.send_message(chat_id, f"Вы выбрали класс: {class_choice}. Теперь выберите профессию:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('set_profession:'))
def set_profession(call):
    chat_id = call.message.chat.id
    profession_choice = call.data.split(':')[1]
    user_states[chat_id]['profession'] = profession_choice

    user_info = user_states.pop(chat_id)
    initial_weapon = give_initial_weapon(user_info['class'])
    new_user_data = {
        'name': user_info['name'],
        'race': user_info['race'],
        'class': user_info['class'],
        'profession': profession_choice,
        'level': 1,
        'experience': 0,
        'strength': 10,
        'dexterity': 10,
        'intelligence': 10,
        'stamina': 10,
        'gold': 0,  # Начальное золото
        'inventory': [initial_weapon],  # Начальный инвентарь
        'health': 100,  # Начальное здоровье
        'waiting_for_bribe_confirmation': False,
        'waiting_for_alms_confirmation': False,
        'location': "портленд",  # Начальная локация - Портленд
        'sublocation': "таверна"  # Начальная подлокация - Таверна
    }
    save_user_data(chat_id, new_user_data)

    markup = InlineKeyboardMarkup()
    start_quest_button = InlineKeyboardButton("Начать квест", callback_data='start_quest')
    markup.add(start_quest_button)

    bot.send_message(chat_id, (f"Персонаж создан! Ваш герой: {user_info['name']}, {user_info['race']} {user_info['class']} "
                               f"с профессией {profession_choice}. Ваше начальное оружие: {initial_weapon}. "
                               "Нажмите ниже, чтобы начать ваше первое приключение."), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'create_character':
        create_character(call.message)
    elif call.data == 'start_quest':
        start_quest(call.message)
    elif call.data == 'accept_quest':
        accept_quest(call)
    elif call.data == 'refuse_quest':
        refuse_quest(call)
    elif call.data.startswith('move_to:'):
        move_to(call)
    elif call.data.startswith('do_action:'):
        do_action(call)
    elif call.data == 'pay':
        pay(call)
    elif call.data == 'next_quest':
        next_quest(call)
    elif call.data == 'secret_mission':
        secret_mission(call)
    elif call.data == 'help_villager':
        help_villager(call)

@bot.message_handler(commands=['start_quest'])
def start_quest(message):
    chat_id = message.chat.id
    user_data = get_user_data(chat_id)
    if not user_data:
        bot.reply_to(message, "Сначала создайте персонажа!")
        return

    user_data['gold'] = 0  # Начальное золото
    user_data['inventory'] = []  # Начальный инвентарь
    user_data['health'] = 100  # Начальное здоровье
    user_data['waiting_for_bribe_confirmation'] = False
    user_data['waiting_for_alms_confirmation'] = False
    user_data['location'] = "портленд"
    user_data['sublocation'] = "таверна"
    save_user_data(chat_id, user_data)

    # Начальный сюжет
    markup = InlineKeyboardMarkup()
    pay_button = InlineKeyboardButton("Заплатить", callback_data='pay')
    markup.add(pay_button)
    bot.send_message(chat_id, ("Вы сидите в таверне, наслаждаясь теплом и уютом, с кружкой эля в руке. "
                               "Время пролетает незаметно, и вы погружаетесь в мысли о великих приключениях. "
                               "Но вот беда, у вас нет денег, чтобы расплатиться. Хозяин таверны, заметив ваше положение, "
                               "подходит к вам и говорит: 'Это будет стоить 10 золотых. Заплатите сейчас.'"), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'pay')
def pay(call):
    chat_id = call.message.chat.id
    user_data = get_user_data(chat_id)
    
    if user_data['gold'] >= 10:
        user_data['gold'] -= 10
        save_user_data(chat_id, user_data)
        bot.send_message(chat_id, "Вы успешно заплатили за свой напиток и остались без денег.")
    else:
        markup = InlineKeyboardMarkup()
        accept_quest_button = InlineKeyboardButton("Согласиться помочь", callback_data='accept_quest')
        refuse_quest_button = InlineKeyboardButton("Отказаться", callback_data='refuse_quest')
        markup.add(accept_quest_button, refuse_quest_button)
        bot.send_message(chat_id, ("У вас недостаточно золота. Хозяин таверны предлагает сделку: "
                                   "если вы поможете ему решить проблему с крысами в доме его брата, "
                                   "он простит ваш долг."), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'accept_quest')
def accept_quest(call):
    chat_id = call.message.chat.id
    user_data = get_user_data(chat_id)
    user_data['quest'] = 'kill_rats'
    save_user_data(chat_id, user_data)

    markup = InlineKeyboardMarkup()
    go_to_house_button = InlineKeyboardButton("Отправиться к дому брата", callback_data='move_to:house')
    markup.add(go_to_house_button)
    bot.send_message(chat_id, ("Вы согласились помочь хозяину таверны. Он благодарит вас и указывает дорогу "
                               "к дому его брата, где завелись крысы."), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'refuse_quest')
def refuse_quest(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, ("Вы отказались от предложения хозяина таверны. Он недоволен, но позволяет вам уйти, "
                               "пригрозив не возвращаться без денег."))

@bot.callback_query_handler(func=lambda call: call.data.startswith('move_to:'))
def move_to(call):
    chat_id = call.message.chat.id
    location = call.data.split(':')[1]
    user_data = get_user_data(chat_id)
    
    if location == 'house':
        user_data['sublocation'] = 'дом брата'
        save_user_data(chat_id, user_data)

        markup = InlineKeyboardMarkup()
        fight_rats_button = InlineKeyboardButton("Сражаться с крысами", callback_data='do_action:fight_rats')
        explore_house_button = InlineKeyboardButton("Осмотреть дом", callback_data='do_action:explore_house')
        markup.add(fight_rats_button, explore_house_button)
        bot.send_message(chat_id, ("Вы прибыли к дому брата хозяина таверны. Дом выглядит старым и заброшенным. "
                                   "Вы слышите шорох внутри."), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('do_action:'))
def do_action(call):
    chat_id = call.message.chat.id
    action = call.data.split(':')[1]
    
    if action == 'fight_rats':
        bot.send_message(chat_id, "Вы вступаете в бой с крысами. После напряженной борьбы вы побеждаете их всех.")
        complete_quest(chat_id)
    elif action == 'explore_house':
        bot.send_message(chat_id, "Вы осматриваете дом и находите старый сундук. Внутри вы находите немного золота и древний амулет.")
        user_data = get_user_data(chat_id)
        user_data['gold'] += 5
        user_data['inventory'].append('древний амулет')
        save_user_data(chat_id, user_data)

def complete_quest(chat_id):
    user_data = get_user_data(chat_id)
    if user_data['quest'] == 'kill_rats':
        user_data['quest'] = 'completed'
        save_user_data(chat_id, user_data)
        
        markup = InlineKeyboardMarkup()
        return_to_tavern_button = InlineKeyboardButton("Вернуться в таверну", callback_data='move_to:tavern')
        markup.add(return_to_tavern_button)
        bot.send_message(chat_id, ("Вы успешно выполнили задание. Пора вернуться в таверну к хозяину и сообщить о выполнении."), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'move_to:tavern')
def return_to_tavern(call):
    chat_id = call.message.chat.id
    user_data = get_user_data(chat_id)
    user_data['sublocation'] = 'таверна'
    save_user_data(chat_id, user_data)

    markup = InlineKeyboardMarkup()
    next_quest_button = InlineKeyboardButton("Получить следующее задание", callback_data='next_quest')
    markup.add(next_quest_button)
    bot.send_message(chat_id, ("Вы возвращаетесь в таверну и сообщаете хозяину о выполнении задания. Он благодарит вас и прощает долг. "
                               "Вы чувствуете, что это только начало ваших приключений."), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'next_quest')
def next_quest(call):
    chat_id = call.message.chat.id
    markup = InlineKeyboardMarkup()
    secret_mission_button = InlineKeyboardButton("Секретная миссия", callback_data='secret_mission')
    help_villager_button = InlineKeyboardButton("Помочь жителю деревни", callback_data='help_villager')
    markup.add(secret_mission_button, help_villager_button)
    bot.send_message(chat_id, ("Хозяин таверны предлагает вам выбрать следующее задание: "
                               "'У меня есть несколько предложений для тебя. Ты можешь выбрать, что тебе больше по душе.'"), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'secret_mission')
def secret_mission(call):
    chat_id = call.message.chat.id
    user_data = get_user_data(chat_id)
    user_data['quest'] = 'secret_mission'
    save_user_data(chat_id, user_data)
    markup = InlineKeyboardMarkup()
    explore_castle_button = InlineKeyboardButton("Исследовать замок", callback_data='move_to:castle')
    markup.add(explore_castle_button)
    bot.send_message(chat_id, ("Вы выбрали секретную миссию. Хозяин таверны шепчет вам: 'Есть слухи о сокровищах, спрятанных в старом замке. "
                               "Но будь осторожен, говорят, что он охраняется привидениями.'"), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'help_villager')
def help_villager(call):
    chat_id = call.message.chat.id
    user_data = get_user_data(chat_id)
    user_data['quest'] = 'help_villager'
    save_user_data(chat_id, user_data)
    markup = InlineKeyboardMarkup()
    go_to_farm_button = InlineKeyboardButton("Отправиться на ферму", callback_data='move_to:farm')
    markup.add(go_to_farm_button)
    bot.send_message(chat_id, ("Вы решили помочь жителю деревни. Хозяин таверны рассказывает: 'Местный житель просил помощи в защите его фермы от бандитов. "
                               "Ему срочно нужна помощь.'"), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('move_to:'))
def move_to(call):
    chat_id = call.message.chat.id
    location = call.data.split(':')[1]
    user_data = get_user_data(chat_id)
    
    if location == 'castle':
        user_data['sublocation'] = 'замок'
        save_user_data(chat_id, user_data)

        markup = InlineKeyboardMarkup()
        fight_ghosts_button = InlineKeyboardButton("Сражаться с привидениями", callback_data='do_action:fight_ghosts')
        explore_castle_button = InlineKeyboardButton("Исследовать замок", callback_data='do_action:explore_castle')
        markup.add(fight_ghosts_button, explore_castle_button)
        bot.send_message(chat_id, ("Вы прибыли к старому замку. Он выглядит зловеще и заброшенно. "
                                   "Вы чувствуете холодный ветер, проходящий сквозь стены."), reply_markup=markup)
    
    elif location == 'farm':
        user_data['sublocation'] = 'ферма'
        save_user_data(chat_id, user_data)

        markup = InlineKeyboardMarkup()
        fight_bandits_button = InlineKeyboardButton("Сражаться с бандитами", callback_data='do_action:fight_bandits')
        explore_farm_button = InlineKeyboardButton("Исследовать ферму", callback_data='do_action:explore_farm')
        markup.add(fight_bandits_button, explore_farm_button)
        bot.send_message(chat_id, ("Вы прибыли на ферму. Житель деревни встречает вас с надеждой в глазах. "
                                   "Ферма выглядит запущенной, и вы слышите шум, доносящийся из полей."), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('do_action:'))
def do_action(call):
    chat_id = call.message.chat.id
    action = call.data.split(':')[1]
    user_data = get_user_data(chat_id)

    if action == 'fight_ghosts':
        bot.send_message(chat_id, "Вы вступаете в бой с привидениями. Они кажутся грозными, но вы используете все свои силы и побеждаете их.")
        user_data['quest'] = 'completed_secret_mission'
        save_user_data(chat_id, user_data)
        bot.send_message(chat_id, "Вы успешно завершили секретную миссию, найдя сокровища в замке! Вы возвращаетесь с богатством.")
    elif action == 'explore_castle':
        bot.send_message(chat_id, "Вы исследуете замок и находите старые записи, раскрывающие тайну древнего рода.")
        user_data['inventory'].append('древние записи')
        save_user_data(chat_id, user_data)
    elif action == 'fight_bandits':
        bot.send_message(chat_id, "Вы вступаете в бой с бандитами. После жестокой схватки вы победили их и защитили ферму.")
        user_data['quest'] = 'completed_help_villager'
        save_user_data(chat_id, user_data)
        bot.send_message(chat_id, "Вы успешно защитили ферму. Житель деревни благодарит вас за помощь.")
    elif action == 'explore_farm':
        bot.send_message(chat_id, "Вы осматриваете ферму и находите спрятанные припасы, которые могут пригодиться в будущем.")
        user_data['inventory'].append('фермерские припасы')
        save_user_data(chat_id, user_data)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_data = get_user_data(chat_id)

    if not user_data:  # Проверка наличия персонажа у пользователя
        bot.reply_to(message, "Сначала создайте персонажа и начните квест /start_quest!")
        return

    # Извлечение данных о локации и подлокации. Это нужно делать после проверки user_data
    current_location = user_data.get('location')
    current_sublocation = user_data.get('sublocation')

    if not current_location or not current_sublocation:
        bot.reply_to(message, "Начните квест! /start_quest")
        return

    location_data = game_world.get(current_location)
    if not location_data:  # Если локации не существует
       bot.reply_to(message, "Вы в неизвестном месте!")
       return

    sublocation_data = location_data['sublocations'].get(current_sublocation)
    if not sublocation_data:  # Если подлокации не существует
         bot.reply_to(message, "Вы в неизвестном месте!")
         return

    # Все проверки перенесены вверх

    if message.text == "/stats":  # Вывод статистики
        show_stats(message)
        return

    available_actions = sublocation_data.get('available_actions', [])

    if message.text in [act["action"] for act in available_actions]:  # Проверка доступных действий
        process_action(bot, message, user_data, message.text, sublocation_data)

    elif message.text in sublocation_data.get("connections", {}):
        user_data['sublocation'] = sublocation_data['connections'][message.text]
        save_user_data(chat_id, user_data)
        new_sublocation_data = game_world[user_data['location']]['sublocations'][user_data['sublocation']]
        bot.reply_to(message, f"Вы перешли в: {new_sublocation_data['name']}.\n{new_sublocation_data['description']}")

    elif message.text in location_data.get("connections", {}):
        user_data['location'] = location_data['connections'][message.text]
        user_data['sublocation'] = list(game_world[user_data['location']]['sublocations'].keys())[0]
        save_user_data(chat_id, user_data)
        new_location_data = game_world[user_data['location']]['sublocations'][user_data['sublocation']]
        bot.reply_to(message, f"Вы прибыли в: {game_world[user_data['location']]['name']}, {new_location_data['name']}. {new_location_data['description']}")

    elif message.text.startswith("Купить"):  # Обработка покупки у торговца
        item_name = message.text.split("(")[0].strip()[7:]  # Извлекаем название предмета
        item_price = int(message.text.split("(")[1].split(")")[0].split()[0])  # Извлекаем цену предмета
        buy_from_merchant(bot, message, user_data, item_name, item_price)
        save_user_data(chat_id, user_data)  # Сохраняем данные пользователя

    elif message.text.startswith('атаковать'):  # Атака монстра
        monster = message.text[10:].strip().lower()
        # Код атаки
        if "goblin_hunt" in user_data.get('quests', []) and monster.startswith('гоблин'):
            user_data['inventory'].append("гоблинское ухо")
            bot.reply_to(message, "Вы забрали гоблинское ухо в качестве доказательства.")
            save_user_data(chat_id, user_data)

    elif user_data.get("waiting_for_bribe_confirmation", False) and message.text == "Дать взятку (50 золотых)":  # Обработка взятки стражнику
        user_data['gold'] -= 50
        user_data['bribe_guard'] = True
        user_data['waiting_for_bribe_confirmation'] = False  # Сбрасываем флаг ожидания

        talk_to_guard(bot, message, user_data)
        save_user_data(chat_id, user_data)  # сохраняем данные пользователя

    elif message.text == "Уйти" and user_data.get("waiting_for_bribe_confirmation", False):  # Обработка отказа от взятки
       user_data["waiting_for_bribe_confirmation"] = False  # Сбрасываем флаг ожидания
       bot.send_message(message.chat.id, "Вы решили не давать взятку.")

    else:
        bot.reply_to(message, "Неизвестная команда. Доступные действия: " + ", ".join([act["action"] for act in available_actions] +
                               list(sublocation_data.get('connections', {}).keys()) +
                               list(location_data.get('connections', {}).keys())))

@bot.message_handler(commands=['stats'])
def show_stats(message):
    chat_id = message.chat.id
    user_data = get_user_data(chat_id)

    if not user_data:
        bot.reply_to(message, "Сначала создайте персонажа.")
        return

    stats_message = ""

    # Статусы персонажа (отдельно от статуса Создателя)
    player_statuses = []
    level = user_data.get('level', 1)

    if 1 <= level <= 10:
        player_statuses.append("Новичок")
    elif 11 <= level <= 30:
        player_statuses.append(">> Опытный <<")
    elif 31 <= level <= 50:
        player_statuses.append("✨Ветеран✨")
    elif level >= 51:
        player_statuses.append("⚜️ Легенда ⚜️")

    # Красивый статус Создателя сверху
    if message.from_user.id == 6480088003:
        stats_message += "**꧁༒☬Создатель☬༒꧂**\n\n"
    else:
        stats_message += "" + ", ".join(player_statuses) + "\n"

    stats_message += f"**{user_data['name']}** (Уровень {user_data.get('level', 1)})\n"
    stats_message += f"Раса: {user_data.get('race', '')}\n"
    stats_message += f"Класс: {user_data.get('class', '')}\n"
    stats_message += f"Профессия: {user_data.get('profession', '')}\n\n"

    stats_message += f"Характеристики:\n"
    stats_message += f"💪 Сила: {user_data.get('strength', 0)}\n"
    stats_message += f"🏃 Ловкость: {user_data.get('dexterity', 0)}\n"
    stats_message += f"🧠 Интеллект: {user_data.get('intelligence', 0)}\n"
    stats_message += f"❤️ Выносливость: {user_data.get('stamina', 0)}\n"
    stats_message += f"💰 Золото: {user_data.get('gold', 0)}\n\n"

    stats_message += f"🎒 Инвентарь: {', '.join(user_data.get('inventory', [])) or 'Пусто'}\n\n"

    # Создаем клавиатуру
    markup = InlineKeyboardMarkup()
    inventory_button = InlineKeyboardButton("Инвентарь", callback_data='show_inventory')
    shop_button = InlineKeyboardButton("Магазин", callback_data='open_shop')
    markup.row(inventory_button, shop_button)  # Располагаем кнопки в одной строке
    bot.send_message(chat_id, stats_message, parse_mode='Markdown', reply_markup=markup)  # исправлено

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'refresh_stats':
        updated_stats = get_user_data(chat_id)
        bot.edit_message_text(updated_stats, chat_id=chat_id, message_id=message_id, parse_mode='Markdown', reply_markup=call.message.reply_markup)

    elif call.data == 'show_inventory':
        user_inventory = get_user_data(chat_id).get('inventory', [])
        inventory_message = "Ваш инвентарь:\n" + "\n".join(user_inventory) if user_inventory else "Ваш инвентарь пуст."
        bot.send_message(chat_id, inventory_message)

    elif call.data == 'open_shop':
        shop_items = {"меч": 10, "щит": 15, "зелье": 5}
        shop_message = "Товары в магазине:\n"
        for item, price in shop_items.items():
            shop_message += f"{item}: {price} золота\n"
        markup = InlineKeyboardMarkup()
        for item, price in shop_items.items():
            buy_button = InlineKeyboardButton(f"Купить {item}", callback_data=f'buy_{item}')
            markup.add(buy_button)

        bot.send_message(chat_id, shop_message, reply_markup=markup)

    elif call.data.startswith('buy_'):
        item_name = call.data[4:]
        price = user_data.get(item_name, 10)

        if user_data.get(user_id, {}).get('gold', 0) >= price:
            user_data.setdefault(user_id, {}).setdefault("gold", 0)
            user_data[user_id]['gold'] = user_data.get(user_id, {}).get('gold', 0) - price
            user_data.setdefault(user_id, {}).setdefault('inventory', []).append(item_name)
            bot.answer_callback_query(call.id, f"Вы купили {item_name}!")

        else:
            bot.answer_callback_query(call.id, "Недостаточно золота!")

    elif call.data == 'create_character':
        user_id = call.from_user.id
        if get_user_data(user_id):
            markup = InlineKeyboardMarkup()
            start_quest_button = InlineKeyboardButton("Начать квест", callback_data='start_quest')
            markup.add(start_quest_button)
            bot.reply_to(call.message, "У вас уже есть персонаж.", reply_markup=markup)
            return
        else:
            user_states[user_id] = "waiting_for_name"
            msg = bot.send_message(call.message.chat.id, "Введите имя вашего персонажа:")
            bot.register_next_step_handler(msg, set_name, user_id)
            bot.edit_message_text("Введите имя вашего персонажа:", chat_id=chat_id, message_id=message_id, parse_mode='Markdown', reply_markup=None)

    elif call.data == 'start_quest':
        start_quest(call.message)
        user_data = get_user_data(chat_id)
        current_location = user_data.get('location')
        current_sublocation = user_data.get('sublocation')
        location_data = game_world.get(current_location)
        sublocation_data = location_data['sublocations'].get(current_sublocation)
        bot.send_message(call.message.chat.id, f"{user_data['name']} начинает свое приключение в {game_world[current_location]['name']}, в {game_world[current_location]['sublocations'][current_sublocation]['name']}.")

bot.polling(none_stop=True)

