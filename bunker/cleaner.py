# удаляем старые файлы игры перед генерацией новых

from os import listdir, remove, path


# ВАЖНО!!!
# если запускать код с этого же файла нужно в начало каждого пути дописать ../ (шаг назад на одну директорию)
# если запускать код с файла bot_main.py - ничего дописывать не надо :)


def clear_dis():  # удаляем файл с катастрофой
    try:
        clear_dir = 'files/'  # путь к файлу
        filelist = [f for f in listdir(clear_dir)]  # добавляем все файлы из директории в список
        for f in filelist:  # для файла с названием disaster.txt удаляем его
            if f == 'disaster.txt':
                remove(path.join(clear_dir, f))  # удаляем файл
    except:
        pass


def clear_bun():  # удаляем файл с описанием бункера
    try:
        clear_dir = 'files/'
        filelist = [f for f in listdir(clear_dir)]
        for f in filelist:
            if f == 'shelter.txt':
                remove(path.join(clear_dir, f))
    except:
        pass


# удаляем файл с картой игрока которая создается при нажатии на кнопку "Карта игрока"
def clear_single_card():
    try:
        clear_dir = 'files/'
        filelist = [f for f in listdir(clear_dir)]
        for f in filelist:
            if f == 'player_card.txt':
                remove(path.join(clear_dir, f))
    except:
        pass


def clear_card():  # удаляем файлы с характеристиками персонажей
    try:
        clear_dir = 'files/players/'
        filelist = [f for f in listdir(clear_dir)]
        for f in filelist:
            if f != 'disaster.txt' and f != 'shelter.txt' and f != 'player_files.zip':
                remove(path.join(clear_dir, f))
    except:
        pass


def clear_zip():
    try:
        clear_dir = 'files/'
        filelist = [f for f in listdir(clear_dir)]
        for f in filelist:
            if f == 'game_bunker.zip':
                remove(path.join(clear_dir, f))
    except:
        pass
