
import telebot
import firebase_admin
from firebase_admin import credentials, firestore

# Замените на ваш путь к файлу ключей
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

API_TOKEN = '7797224960:AAGcX4Wihc5ZsJUgFB3BLnBVuFvvtUyBILc'  # НЕБЕЗОПАСНО! Храните токен в переменных окружения.
bot = telebot.TeleBot(API_TOKEN)

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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Используйте /create_character.")

@bot.message_handler(commands=['create_character'])
def create_character(message):
    chat_id = message.chat.id
    if get_user_data(chat_id):
        bot.reply_to(message, "У вас уже есть персонаж. Используйте /start_quest.")
        return

    msg = bot.reply_to(message, "Введите имя вашего персонажа:")
    bot.register_next_step_handler(msg, set_name, chat_id)

def set_name(message, chat_id):
    name = message.text.strip()
    msg = bot.reply_to(message, f"Имя: {name}. Выберите класс (воин, маг, вор):")
    bot.register_next_step_handler(msg, set_class, chat_id, name)

def set_class(message, chat_id, name):
    class_choice = message.text.strip().lower()
    if class_choice not in ['воин', 'маг', 'вор']:
        msg = bot.reply_to(message, "Неверный класс. Попробуйте ещё раз.")
        bot.register_next_step_handler(msg, set_class, chat_id, name)
        return

    save_user_data(chat_id, {'name': name, 'class': class_choice, 'level': 1, 'experience': 0})
    bot.reply_to(message, f"Персонаж создан! Используйте /start_quest.")

@bot.message_handler(commands=['start_quest'])
def start_quest(message):
    chat_id = message.chat.id
    user_data = get_user_data(chat_id)
    if not user_data:
        bot.reply_to(message, "Сначала создайте персонажа!")
        return
    bot.reply_to(message, f"{user_data['name']} отправляется в приключение...")

bot.polling(none_stop=True)