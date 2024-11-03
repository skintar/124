import random
import telebot # important! need to add telebot import

def talk_to_innkeeper(bot, message, user_data):
    bot.reply_to(message, "Хозяин таверны,  протирая  кружку,  приветливо  вам  улыбается.  'Ну,  путник,  чем  могу  быть  полезен?  Слышал  истории  о  странных  вещах,  творящихся  в  Темном  лесу.  Говорят,  гоблины  совсем  распоясались.  Может,  тебе  интересно  будет  заняться  ими?  За  каждую  гоблинскую  голову  я  готов  хорошо  заплатить.'")

    # Пример добавления квеста
    user_data['quests'] = user_data.get('quests', [])  # Инициализируем список квестов, если его нет.
    if "goblin_hunt" not in user_data['quests']:  #  Проверяем,  не  взят ли квест
        user_data['quests'].append("goblin_hunt")
        bot.send_message(message.chat.id, "Вы получили квест: Охота на гоблинов!")




def talk_to_guard(bot, message, user_data): # important changes. Now if "дать взятку" exists only keyboard is created without logic! All logic needs to be done in the main bot file.
     if user_data.get("bribe_guard"):
        bot.send_message(message.chat.id, "Стражник пропускает вас без лишних вопросов. 'Проходите, но будьте осторожны за стенами.'")
        user_data["bribe_guard"] = False  #  Взятка  использована

     elif user_data.get('gold', 0) >= 50:
        # создаем клавиатуру. adding necessary dialog
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        markup.add(telebot.types.KeyboardButton("Дать взятку (50 золотых)"))
        markup.add(telebot.types.KeyboardButton("Уйти"))  #  Important:  всегда  хорошо  иметь  возможность  выйти  из  диалога

        bot.send_message(message.chat.id, "Хмм...  вижу,  у  вас  найдется, чем убедить меня. 50 золотых, и я забуду, что видел вас.", reply_markup=markup)
        #  Обработку  нажатия  кнопки  нужно  делать  в handle_message


     else:
        bot.reply_to(message, "У  вас нет нужных документов и вы не можете дать взятку.  Возвращайтесь, когда они у вас появятся.")

def talk_to_druid(bot, message, user_data):
    bot.reply_to(message, "Друид,  одетый  в  одежды  из  листьев  и  кожи,  приветствует  вас  кивком  головы. 'Мир  тебе,  путник.  Лес  полон  тайн  и  опасностей.  Будь  осторожен.'  Он  предлагает  вам  выпить  целебного  отвара,  который  восстановит  ваши  силы.")
    #  Пример  восстановления  здоровья (замените  своими  переменными)
    user_data['health'] = user_data.get('health', 100)
    user_data['health'] = min(100, user_data['health'] + 20)  #  Не  больше  максимального
    bot.send_message(message.chat.id,  f"Ваше здоровье восстановлено до {user_data['health']}.")

def talk_to_oracle(bot, message, user_data):
    predictions = [
        "Вскоре ты найдешь то, что ищешь.",
        "Остерегайся темных пещер.",
        "Твое будущее туманно. Будь осторожен.",
        "Тебя ждет великая победа.",
        "В твоей жизни грядут перемены."
    ]

    prediction = random.choice(predictions)

    bot.reply_to(message, f"Оракул пристально смотрит на вас и произносит: '{prediction}'")

def talk_to_merchant(bot, message, user_data):

    items = {"зелье здоровья": 10, "меч": 50, "щит": 30}
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)



    for item, price in items.items():
       markup.add(telebot.types.KeyboardButton(f"Купить {item} ({price} золотых)"))
    markup.add(telebot.types.KeyboardButton('Уйти'))




    bot.reply_to(message, f"Торговец  раскладывает свой товар. 'Что вас интересует,  путник? У меня  есть {' ,'.join(items.keys())}.'",  reply_markup=markup)
    # Обработка нажатия кнопки "купить" делается в handle_message.

def buy_from_merchant(bot, message, user_data, item_name, item_price):
   if user_data.get('gold', 0) >= item_price:
       user_data['gold'] -= item_price
       #  Добавляем  предмет  в  инвентарь  игрока (пример,  доработайте  логику  инвентаря)
       user_data['inventory'] = user_data.get('inventory', [])
       user_data['inventory'].append(item_name)  # should have separate variable, since you're giving away and taking values
       bot.reply_to(message, f"Вы купили {item_name}.  Он добавлен в ваш инвентарь.  У вас осталось {user_data['gold']} золотых.")
   else:
       bot.reply_to(message, "У вас недостаточно золота.")

def gamble_with_sailor(bot, message, user_data):

    bet = 10

    user_roll = random.randint(1, 6) + random.randint(1, 6)
    sailor_roll = random.randint(1, 6) + random.randint(1, 6)

    if user_roll > sailor_roll:
        bot.send_message(message.chat.id, f"Вы выбросили {user_roll}, моряк — {sailor_roll}. Вы выиграли {bet}!")
        user_data['gold'] = user_data.get('gold', 0) + bet  # Adding gold logic
    elif user_roll < sailor_roll:
        bot.send_message(message.chat.id, f"Вы выбросили {user_roll}, моряк — {sailor_roll}. Вы проиграли {bet}!")
        user_data['gold'] = user_data.get('gold', 0) - bet  # Removing gold logic
    else:
        bot.send_message(message.chat.id, f"Ничья ({user_roll}:{sailor_roll}). Деньги возвращены.")	



def talk_to_beggar(bot, message, user_data):



    if user_data.get("gold", 0) > 0:

        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Дать милостыню'))
        markup.add(telebot.types.KeyboardButton('Пройти мимо')) # important! adding one more action and removing earlier given alms logic out of if

        bot.reply_to(message, "Нищий просит у вас милостыню. Что вы сделаете?", reply_markup=markup) # adding necessary dialog here for the button



    else:
        bot.reply_to(message, "Нищий просит у вас милостыню, но у вас нет золота.")


def talk_to_old_man(bot, message, user_data):

      bot.reply_to(message,"Старик  приветливо кивает, попыхивая трубкой и рассказывает о своей жизни, о путешествиях, о опасностях и радостях, делится житейской мудростью:")


      wisdoms = [
        "В жизни, как и на карте мира - есть тропы, которые приведут к удаче. Найти верные пути тебе поможет твоя совесть, как компас, она направит тебя к чести и добру",
         "Знания — это твой самый ценный рюкзак, чем он больше наполнен, тем богаче твой жизненный путь и опыт, как карта приключений, которую стоит беречь.",
         "Твои союзники - не только те, кто делит хлеб, но и те, кто делит трудности, они будут опорой на тернистых дорогах и верными товарищами",
         "Не всегда дорога легка и быстра. Стойкость - твой лучший конь, на нем ты преодолеешь крутые подъемы и доберешься до желанной вершины."


       ]
      bot.send_message(message.chat.id, random.choice(wisdoms))


def give_alms(bot, message, user_data):  # Новая функция для обработки милостыни
    user_data['gold'] -= 1
    bot.reply_to(message, "Вы дали нищему монетку. Он благодарит вас.")