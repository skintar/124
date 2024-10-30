import telebot

API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

users = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в QuestMasterBot! Используйте команду /create_character, чтобы создать персонажа.")

@bot.message_hand
ler(commands=['create_character'])
def create_character(message):
    chat_id = message.chat.id
    if chat_id in users:
        bot.reply_to(message, "У вас уже есть персонаж. Используйте /start_quest для начала приключения.")
        return
    
    msg = bot.reply_to(message, "Введите имя вашего персонажа:")
    bot.register_next_step_handler(msg, set_name)

def set_name(message):
    chat_id = message.chat.id
    name = message.text.strip()
    users[chat_id] = {'name': name, 'class': None, 'level': 1, 'experience': 0}
    msg = bot.reply_to(message, f"Имя вашего персонажа: {name}. Выберите класс (воин, маг, вор):")
    bot.register_next_step_handler(msg, set_class)

def set_class(message):
    chat_id = message.chat.id
    class_choice = message.text.strip().lower()
    if class_choice not in ['воин', 'маг', 'вор']:
        msg = bot.reply_to(message, "Пожалуйста, выберите класс: воин, маг или вор.")
        bot.register_next_step_handler(msg, set_class)
        return
    
    users[chat_id]['class'] = class_choice
    bot.reply_to(message, f"Вы выбрали класс {class_choice}. Ваш персонаж готов! Используйте /start_quest для начала приключения.")

@bot.message_handler(commands=['start_quest'])
def start_quest(message):
    chat_id = message.chat.id
    if chat_id not in users:
        bot.reply_to(message, "Сначала создайте персонажа с помощью /create_character.")
        return
    
    bot.reply_to(message, f"{users[chat_id]['name']} отправляется в приключение. Вы встретили странника на пути. Что вы сделаете? (атаковать/поговорить/уйти)")
    # Здесь можно добавить логику для обработки выбора пользователя и развития квеста.

bot.polling(none_stop=True)