# генерация убежища

from pathlib import Path, WindowsPath
from random import choice, randint
from datetime import date
from bunker import cleaner

# ВАЖНО!!!
# если запускать код с этого же файла нужно в начало каждого пути дописать ../ (шаг назад на одну директорию)
# если запускать код с файла bot_main.py - ничего дописывать не надо :)

on_mars = None


def get_bunker():
    global on_mars

    cleaner.clear_bun()

    bun_dir = 'src/bunker/'
    there_is = []
    size = 0

    for addon in Path(bun_dir).glob('*'):  # для каждого параметра в бункере делаем свои условия выпадения
        # если текущий файл = guns.txt, в список there_is рандомно добавляем одно оружие с 10% шансом
        if addon == WindowsPath(bun_dir + 'guns.txt') and randint(0, 101) in range(0, 11):
            gun_list = [line.rstrip() for line in open(addon, encoding='utf-8').readlines()]
            there_is.append(choice(gun_list))  # добавляем одно оружие из всего списка
        # если текущий файл = item.txt, в список there_is добавляем каждый предмет с 15% шансом
        if addon == WindowsPath(bun_dir + 'items.txt'):
            item_list = [line.rstrip() for line in open(addon, encoding='utf-8').readlines()]
            for item in item_list:
                if randint(0, 101) in range(0, 16):
                    there_is.append(item)  # добавляем предмет в список с 15% шансом
        # если текущий файл = rooms.txt, в список there_is добавляем каждую комнату с 30% шансом
        if addon == WindowsPath(bun_dir + 'rooms.txt'):
            room_list = [line.rstrip() for line in open(addon, encoding='utf-8').readlines()]
            for room in room_list:
                if randint(0, 101) in range(0, 31):
                    there_is.append(room)  # добавляем комнату в список с 30% шансом
                    size += 1  # в дальнейшем поможет узнать размер бункера
    # устанавливаем размер бункера
    while size < 4:
        size += 1
    size = f'Размер бункера {size * 20} кв/м'

    # если катастрофа == "Mars One" выполняем кусок кода if
    if on_mars is True:
        can_leave = f'Вы никогда не вернетесь на Землю'
    else:  # если катастрофа != "Mars One" выполняем кусок кода else
        # рандомим длительность проживания в бункере (плюсуем число от 5 до 99 к текущему году игрока)
        # что бы узнать текущий год игрока импортируем date из datetime и используем функцию date.today().year
        can_leave = f'Вы сможете выйти наружу в {date.today().year + randint(5, 100)} году'

    with open('files/shelter.txt', 'w', encoding='utf-8') as file:
        file.write(f''' - - - Убежище - - - \n{size}\n{can_leave}\nВ бункере есть: {', '.join(there_is)}''')

# get_bunker()
