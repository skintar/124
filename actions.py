from npc import *  # Импорт функций из npc.py
import random

def process_action(bot, message, user_data, action_name, sublocation_data):
     for action in sublocation_data.get('available_actions', []):
          if action.get('action') == action_name:

               function_name = action.get('function')

               if function_name:

                  globals()[function_name](bot, message, user_data)

                  return

          elif "item_name" in action and action["action"]==action_name and  "price" in action :

                function_to_call = globals()[action["function"]]

                try:

                    function_to_call(bot, message, user_data,action['item_name'], action['price']  )

                    return

                except Exception as e:

                    print(f"Произошла ошибка:{e}, arguments {action}, func_name {action['function']} ")

                    bot.reply_to(message, "Произошла ошибка.")

          elif 'target' in action and action["action"]==action_name:

                function_name = globals()[action.get("function")]

                try:

                    function_name(bot, message, user_data, action.get("target"), action.get("damage")  )

                    return

                except Exception as e:

                    print(f"Произошла ошибка: {e} ,  {action}, {action['function']}")

                    bot.send_message(message.chat.id, "Произошла ошибка при вызове функции NPC ")

          elif 'npc_name' in action and action['action'] == action_name:  # Actions with npc

             globals()[action['function']](bot, message, user_data, action.get('npc_name'))

             return # adding return to function after npc functions

          elif  'item_name' in action and action['action'] == action_name and 'function' in action:

               try:
                   globals()[action['function']](bot, message, user_data, action['item_name'])

                   return

               except Exception as e:

                    print(f"Произошла ошибка: {e}")

                    bot.send_message(message.chat.id,f"Ошибка: {e}")

def examine(bot, message, user_data):  # action for looking at places like in previous example
    current_location = user_data.get('location')
    current_sublocation = user_data.get('sublocation')
    if current_location and current_sublocation and game_world.get(current_location) and game_world[current_location]['sublocations'].get(current_sublocation):  # Checking all steps to locate text without possible crash!
        bot.reply_to(message, game_world[current_location]['sublocations'][current_sublocation]['description'])  # important using reply_to since we have our needed bot here in message variable
    else: # and else if the key doesn't exist
       bot.send_message(message.chat.id, "Я не понимаю, что нужно осмотреть. \nНачните игру /start ")

def buy_drink(bot, message, user_data, drink_name, price=10):
     # Добавьте логику покупки напитка.  Измените цену, если нужно.
       if user_data.get('gold',0)>= price:

            user_data["gold"]-=price

            bot.reply_to(message, f"Вы купили {drink_name} за {price} золотых. Осталось {user_data['gold']}")

       else: # changing from chat_id to reply_to message here again
          bot.reply_to(message, "У вас недостаточно денег") # replying when money not enough.

def gamble(bot, message, user_data):  #  Пример  игры  в  кости
       gamble_with_sailor(bot,message,user_data)

def listen_stories(bot, message, user_data): # using sailor for stories.
   bot.reply_to(message,"Моряк  радушно приглашает вас  присесть и послушать захватывающую историю.")  # changed using message['text'] here, more correct

   wisdoms = [
     "В бурных морях судьбы, как старый корабль, я плыл по волнам жизни. Встречал штормы и бури, терпел крушения, терял надежду. Но,  благодаря моей стойкости и вере в лучшее, смог выжить",
        "А помнишь тот бой у берегов Тортуги? Там мы с командой в пух и прах разнесли флот испанцев. И все благодаря нашему капитану, умнейшему из людей",
         "Когда мы причалили к Золотому острову, то перед нами предстала диковинная красота - деревья с золотыми плодами, дома, словно отлитые из янтаря и серебра, воздух напоен благоуханием райских цветов",
         "А был я в краю вечной зимы, и там солнце - словно замороженное - и не светит совсем. И мороз там трещит,  и земля - тверда как камень. Жил в краю том ледяной народ - хранители древних знаний."
      ]

   bot.send_message(message.chat.id,random.choice(wisdoms))

def give_bribe(bot, message, user_data):  # updated example
    if user_data.get('gold', 0) >= 50: # guard needs to be able to take bribe
      user_data['waiting_for_bribe_confirmation'] = True


      talk_to_guard(bot,message,user_data)




    else:


       bot.reply_to(message, "У вас недостаточно золота.")

def meditate(bot, message, user_data):

    bot.reply_to(message, "Вы медитируете, восстанавливая ману.")

    user_data['mana'] = user_data.get('mana', 0) + 20  #  Пример восстановления маны.  Замените  своими значениями.
    # correctly updating using get and then changing for correct work. In future can be removed, up to user to test when doing. Should do if not defined because get is for taking values or returning default value if something doesn't exist.



    bot.send_message(message.chat.id, f"Ваша мана: {user_data['mana']}")  # important, check for yourself when it exists. Otherwise this value is shown as available after doing it for the first time and it is confusing. Can remove after, depends how user prefers, up to self.





def cross_pass(bot, message, user_data):

    bot.reply_to(message, "Вы проходите горный перевал...")




    if "теплая одежда" not in user_data.get('inventory', []):

        bot.send_message(message.chat.id, "Вы замерзли,  переходя  перевал,  и потеряли  10  здоровья!")

        user_data['health'] = max(0, user_data.get('health', 100) - 10)  # Не  меньше  нуля





def make_camp(bot, message, user_data):


 bot.reply_to(message, "Вы  разбиваете лагерь  и  восстанавливаете  20  здоровья.")


 user_data['health'] = min(100, user_data.get('health', 0) + 20)

def explore_cave(bot,message, user_data):




       if random.random() < 0.3:  #  30%  шанс  найти  что-то



           item = random.choice(["лед", "старый меч"])  #  Случайный предмет

           user_data['inventory'].append(item)  # better code, adding only item.


           bot.send_message(message.chat.id, f"Вы  нашли  {item}!")



       else:


           bot.reply_to(message,"Вы  исследовали пещеру, но ничего  не  нашли.")


def mine_ice(bot, message, user_data):
       #  Добавьте проверку на  наличие  кирки  в  инвентаре
       bot.reply_to(message, "Вы добываете лед.")
       user_data['inventory'] = user_data.get('inventory', [])
       user_data['inventory'].append('лед')

def drink_water(bot, message, user_data):
    bot.reply_to(message, "Вы напились свежей воды и восстановили 10 здоровья.")
    user_data['health'] = min(100, user_data.get('health', 0) + 10)


def relax(bot, message, user_data):
    bot.reply_to(message, "Вы отдыхаете в тени пальм и восстанавливаете 15 здоровья.")
    user_data['health'] = min(100, user_data.get('health', 0) + 15)


def explore_temple(bot, message, user_data):
  if  random.random() < 0.2:  #  20% шанс  найти что-то
     item = random.choice(["золотой идол",  "старинный свиток"])
     user_data['inventory'].append(item) # better and correct implementation. Should look same as rest or similar and if needed extra parameter added for correct work and then you would see which needs work
     bot.send_message(message.chat.id,f"Вы  нашли  {item}!")

  else:
       bot.reply_to(message,"Вы исследовали  храм,  но ничего  не  нашли.")


def decipher_hieroglyphs(bot,message, user_data):
 if "старинный свиток" in user_data['inventory']:  # Проверка,  есть  ли  свиток


         bot.send_message(message.chat.id,  "Вы  расшифровали иероглифы:  'Здесь  спрятаны  сокровища!'")


   # Добавить  логику  получения  сокровищ



 else:
    bot.reply_to(message, "У вас нет предмета для расшифровки")


def explore_square(bot, message, user_data):
     if random.random() < 0.1:

         item = random.choice(["зачарованный амулет",  "старинная монета"])


         user_data['inventory'].append(item)  # appending item correctly


         bot.send_message(message.chat.id, f"Вы нашли: {item}!")  # adding what we got here correctly


     else: # and changing where and how we reply here

        bot.reply_to(message, "Вы исследовали  площадь,  но  ничего не нашли.")




def search_artifacts(bot, message, user_data): # example



       if  random.random() <  0.05:  # 5% шанс  найти  редкий  артефакт



           item = "магический  кристалл"  # Пример



           user_data['inventory'].append(item)  # append here instead



           bot.send_message(message.chat.id, f"Вы  нашли  {item}!")



       else:


           bot.reply_to(message, "Вы  ничего не  нашли.")

def explore_dungeon(bot, message, user_data):
    if random.random() < 0.4:
        item = random.choice(["золото", "старый щит"])
        user_data['inventory'] = user_data.get('inventory', [])
        if item == "золото":
            gold_amount = random.randint(10, 30) # give some random gold
            user_data['gold'] = user_data.get('gold', 0) + gold_amount # some gold received
            bot.send_message(message.chat.id, f"Вы нашли {gold_amount} золотых!")
        else:
            user_data['inventory'].append(item)
            bot.send_message(message.chat.id, f"Вы нашли: {item}!")
    else:
        bot.reply_to(message, "Вы исследовали подземелье, но ничего не нашли.")

def fight_rats(bot, message, user_data, target="крысы"):
       rat_health = 30
       damage = user_data.get('strength', 10)
       rat_health -= damage

       if rat_health <= 0:

         bot.reply_to(message, f"Вы убили {target}.")

         user_data['gold'] = user_data.get('gold', 0) + 5 # add some gold for test
         user_data['experience'] = user_data.get('experience', 0) + 10
         bot.send_message(message.chat.id,"Вы получили 5 золотых и 10 опыта.")

         return True

       else:
          bot.reply_to(message, f"Вы атаковали {target}. У них осталось {rat_health} здоровья.")
          return False

def talk(bot, message, user_data, npc_name):


       npc_function = globals()[f"talk_to_{npc_name}"]
       if npc_function:
             npc_function(bot, message, user_data) # don't do message['text']
             return
       bot.reply_to(message, f"NPC '{npc_name}' не найден.")

def buy(bot, message, user_data, item_name, price=None):

    if not price:
        raise ValueError("Ошибка, нет цены.")

    if user_data.get('gold', 0) >= price: # logic to correctly spend and show items left
         user_data['gold'] -= price
         user_data['inventory'] = user_data.get('inventory',[])
         user_data['inventory'].append(item_name)
         bot.reply_to(message, f"Вы купили {item_name} за {price} золотых. У вас осталось {user_data.get('gold',0)} золотых.")  # better code again

    else:

        bot.reply_to(message, "У вас недостаточно золота.")

def use(bot, message, user_data, item_name):
     try:

           use_function = globals()[f"use_{item_name.replace(' ', '_')}"] # correct way
           use_function(bot,message,user_data)
           return

     except KeyError as err:


        bot.reply_to(message, f"Вы не можете использовать '{item_name}'.")

def attack_monster(bot, message, user_data, target="монстр", damage=20):
    strength = user_data.get("strength")
    strength_bonus = user_data.get("strength_bonus", 0)  #  Получаем бонус к силе.  Если его нет,  он равен 0.

    if strength is None:
        bot.reply_to(message, "У вас нет силы для атаки!")
        return

    monster_health = 50  # Здоровье монстра
    damage = damage + (strength + strength_bonus) * 0.2  # Урон зависит от силы + бонус

    monster_health -= damage

    if monster_health <= 0:
        bot.reply_to(message, f"Вы убили {target}.")

        user_data['gold'] = user_data.get('gold', 0) + 10  #  Пример награды
        user_data['experience'] = user_data.get('experience', 0) + 20
        bot.send_message(message.chat.id,  "Вы  получили 10 золотых  и  20 опыта.")

        return 
    bot.reply_to(message, f"{target} имеет {monster_health} жизней. Вы наносите {int(damage)} урона.")


def use_зелье_здоровья(bot, message, user_data): # need to have correctly spaced words so "use" can locate function
   if "зелье здоровья" in user_data.get('inventory',[]):
         user_data['health'] = min(100, user_data.get('health',0) + 20)
         user_data['inventory'].remove("зелье здоровья")
         bot.reply_to(message, f"Вы выпили зелье здоровья. Ваше здоровье: {user_data['health']}.")

   else:
         bot.reply_to(message, "У вас нет зелья здоровья.")

def use_старый_меч(bot, message, user_data):
    bot.reply_to(message, "Вы взмахнули старым мечом.  Он  довольно  тупой.")  # Замените на  логику  боя


def use_теплая_одежда(bot, message, user_data):
    bot.reply_to(message, "Вы надели теплую одежду. Теперь вам  не  страшен  холод.")  #  Можно  добавить  эффект  защиты  от  холода

def use_золотой_идол(bot, message, user_data):

 bot.reply_to(message, "Вы  подняли золотой идол.  Он  тяжелый  и  холодный. Кажется, он реагирует на магию в тебе.")
 #  Добавьте логику использования  идола

def use_старинный_свиток(bot,  message, user_data): # need this, so when scroll is found user doesn't have error from 'use' but has what they typed
   decipher_hieroglyphs(bot,message, user_data)

def use_зачарованный_амулет(bot, message, user_data):
    bot.reply_to(message, "Вы надели зачарованный амулет.  Вы  чувствуете  прилив  сил!")  #  Добавьте  эффект  амулета

def use_старинная_монета(bot,  message,  user_data):
    bot.reply_to(message, "Вы  рассматриваете старинную монету.  На  ней  изображен  незнакомый  герб.")  #  Можно  добавить  историю  монеты

def use_магический_кристалл(bot,  message, user_data):
    bot.reply_to(message, "Вы  сжимаете магический кристалл  в  руке. Он пульсирует  волнами  магии,  наделяя вас силой!")
    user_data['strength_bonus'] = user_data.get('strength_bonus', 0) + 10
    user_data['strength_bonus_turns'] = 3  #  Бонус действует 3 хода
    user_data['inventory'].remove("магический кристалл")

def use_старый_щит(bot, message, user_data):  # Example and usage, correct

       bot.reply_to(message,"Вы  взяли  старый  щит. Он  довольно  прочный. Добавим в инвентарь.")
       if "старый щит" not in user_data['inventory']:

            user_data["inventory"].append("старый щит")
       else:
         bot.send_message(message.chat.id,"У вас уже есть щит в инвентаре")
