# главный файл бота, откуда будет осуществлятся все запросы к боту и его ответы игроку

import telebot
from telebot import types
from time import sleep

from bot_cfg import TOKEN, chat_id

from bunker import disaster, shelter, player, zip_file

bot = telebot.TeleBot(TOKEN)

title = [
    'Пол и возраст', 'Профессия', 'Здоровье',
    'Телосложение', 'Фобия', 'Характер', 'Хобби',
    'Багаж', 'Доп. инфа', 'Карта действия'
]


@bot.message_handler(commands=['start'])  # ответ бота на команды
def send_welcome(msg):
    bot.reply_to(msg, '/start is work', reply_markup=main_kb())


@bot.message_handler(content_types='[text]')  # ответы бота при нажатии на клавиатуру
def bot_answer(msg):
    if msg.text == 'Отмена':
        bot.reply_to(msg, 'Открываю основную клавиатуру', reply_markup=main_kb())

    if msg.text == 'Катастрофа':
        send_dis()  # функция отправляет файл с описанием бункера

    if msg.text == 'Убежище':
        send_bunker()  # функция отправляет файл с описанием убежища

    if msg.text == 'Карта игрока':
        # функция отправляет файл с картой игрока которая создается при нажатии на кнопку "Карта игрока"
        send_single_card()

    if msg.text == 'Играть':
        bot.reply_to(msg, 'Выберите количество играков', reply_markup=inline_kb())

    if msg.text == 'Использовать карту действия':
        bot.reply_to(msg, 'Выберите пункт который нужно заменить', reply_markup=use_card_kb())

    if msg.text in title:  # ответы бота на собития из use_card_kb
        player.get_card()  # генерируем карты с характеристиками персонажа

        # создаем два условия:
        # 1) если сообщение от пользователя есть в списке title
        # 2) индекс сообщения который в списке title равен индексу в списке player.pl_card
        # переменной char_ans присваеваем значение характеристики из списка player.pl_card с индексом
        # индекса сообщения в списке title (player.pl_card[title.index(msg.text)])

        if title.index(msg.text) == 0:
            # так как стаж работы зависит от возраста персонажа - выводим его вместе с возрастом
            char_ans = (player.pl_card[title.index(msg.text)] + player.pl_card[2]).replace('\n', '')
            #                       пол и возраст                 стаж работы
        elif title.index(msg.text) >= 2:
            # условие создано потому что в списке player.pl_card есть переменная стаж работы, а в title - нет
            # (если не писать это условие ответы бота не будет правильно работать)
            char_ans = (player.pl_card[(title.index(msg.text) + 1)])
        else:
            char_ans = (player.pl_card[title.index(msg.text)])

        bot.send_message(chat_id, char_ans, reply_markup=main_kb())


# для удобного использования бота создаем клавиатуру
def main_kb():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn_disaster = types.KeyboardButton('Катастрофа')
    btn_bunker = types.KeyboardButton('Убежище')
    btn_player = types.KeyboardButton('Карта игрока')
    btn_start = types.KeyboardButton('Играть')
    btn_use_card = types.KeyboardButton('Использовать карту действия')

    markup.row(btn_start)
    markup.row(btn_disaster, btn_bunker, btn_player)
    markup.row(btn_use_card)

    return markup


# создаем клавиатуру что бы использовать карту действия (получения новых характеристик персонажа)
def use_card_kb():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    i = 0
    while i < len(title):
        title[i] = title[i]
        i += 1

    # создаем кнопку которая закрывает клавиатуру с характеристиками и открывает основную
    btn_cancel = types.KeyboardButton('Отмена')

    markup.row(title[0], title[1], title[2])
    markup.row(title[3], title[4], title[5], title[6])
    markup.row(title[7], title[8], title[9])

    markup.row(btn_cancel)  # отображаем кнопку

    return markup


# создаем клавиатуру с выбором количества игроков
def inline_kb():
    global pl_num

    # максимальное количество игроков должно быть на 2 больше потому что:
    # 1. range(6, 21) = выводит числа 6 до 20
    # 2. еще +1 нужен для того что бы вывести третий ряд inline клавиатуры

    pl_num = range(6, 32)  # минимальное и максимальное количество играком

    markup = types.InlineKeyboardMarkup()

    inline_btn = []  # переменаня для создания inline клавиатуры
    i = 0  # переменная для итераций

    while i < len(pl_num):  # создаем и выводим на экран (сообщение от бота) inline клавиатуру
        # даный кусок кода генерирует клавиатуру
        inline_btn.append(i)
        btn = types.InlineKeyboardButton(pl_num[i], callback_data=pl_num[i])
        inline_btn[i] = btn

        check_list = (1.0, 2.0, 3.0, 4.0, 5.0)

        # даный кусок кода выводит клавиатуру на экран
        if int(i) / 5 in check_list:
            markup.row(
                inline_btn[i - 5], inline_btn[i - 4], inline_btn[i - 3], inline_btn[i - 2], inline_btn[i - 1]
            )  # один ряд кнопок inline клавиатуры
        i += 1

    return markup


@bot.callback_query_handler(func=lambda call: True)
def ans(call):
    global max_pl
    if call.message:
        for i in pl_num:
            if call.data == str(i):
                max_pl = int(i)
                bot.send_message(chat_id, 'Отлично! Сейчас я Вам отправлю все нужные файлы для игры.')

                send_zip()  # отправляем zip файл

                answer = 'Я отправил Вам архив с описание катастрофы, убежища и картами играков. Приятной игры!'
                bot.send_message(chat_id, answer)


# /*/ функции которые отправляют файлы нужные для игры /*/

def send_dis():  # функция отправляет файл с описанием бункера
    disaster.get_dis()
    dis_doc = open(r'files/disaster.txt', 'rb')

    bot.send_document(chat_id, dis_doc)
    sleep(.5)


def send_bunker():  # функция отправляет файл с описанием убежища
    shelter.get_bunker()
    shelter_doc = open(r'files/shelter.txt', 'rb')

    bot.send_document(chat_id, shelter_doc)
    sleep(.5)


# функция отправляет файл с картой игрока которая создается при нажатии на кнопку "Карта игрока"
def send_single_card():
    player.single_card()
    card_doc = open(r'files/player_card.txt', 'rb')

    bot.send_document(chat_id, card_doc)
    sleep(.5)


def send_zip():  # функция отправляет zip файл для игры
    global max_pl

    disaster.get_dis()  # генерируем катастрофу
    shelter.get_bunker()  # генерируем убежище
    player.write_card(max_pl)  # генерируем карту игрока

    zip_file.create_zip()  # добавляем все файлы в zip файл

    # отправляем zip файл
    zip_doc = open(r'files/game_bunker.zip', 'rb')
    bot.send_document(chat_id, zip_doc)
    sleep(.5)


# бессконечная итерация кода (бот)
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
