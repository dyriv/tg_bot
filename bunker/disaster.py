# генерация катастрофы
from pathlib import Path
from random import choice

from bunker import shelter, cleaner


# ВАЖНО!!!
# если запускать код с этого же файла нужно в начало каждого пути дописать ../ (шаг назад на одну директорию)
# если запускать код с файла bot_main.py - ничего дописывать не надо :)


def get_dis():
    global on_mars

    cleaner.clear_dis()

    dis_dir = 'src/disasters/'  # путь к папке с катастрофами
    # '../files/disaster.txt' - путь к файлу в который записано сгенерированую катастрофу

    # для каждого файла в <dis_dir> (папке со всеми возможными катастрофами) делаем следущее:
    # 1. открываем 2. читаем 3. убираем \n 4. каждый файд добавляем в dis_list
    dis_list = []
    for dis in Path(dis_dir).glob('*'):
        if dis.is_file():
            dis_file = [line.rstrip() for line in open(str(dis), encoding='utf-8').readlines()]
            #                       3                       1                                   2
            dis_list.append(dis_file)  # 4

    cur_dis = ''.join(choice(dis_list))  # выбираем из всех катастроф одну

    # если катастрофа = mars_one.txt выполняем следующий код, в противном случае - скип
    mars_one = open(dis_dir + 'mars_one.txt', 'r', encoding='utf-8').read()
    if cur_dis == mars_one:
        shelter.on_mars = True

    # записуем катастрофу в файл disaster.txt
    with open('files/disaster.txt', 'w', encoding='utf-8') as file:
        file.write(f' - - - Катастрофа - - - \n{cur_dis}\n')

# get_dis()
