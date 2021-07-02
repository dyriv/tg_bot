import zipfile
from os import listdir
from bunker import cleaner


def create_zip():
    file_dir = 'files/players'
    card_list = [f for f in listdir(file_dir)]

    cleaner.clear_zip()  # удаляем старый zip файл

    # создаем zip файл
    zip_name = r'files/game_bunker.zip'
    game_zip = zipfile.ZipFile(zip_name, 'w')

    card = 1

    # добавляем каждый txt файл в zip
    game_zip.write('files/disaster.txt')
    game_zip.write('files/shelter.txt')

    while card < len(card_list) + 1:
        game_zip.write('files/players/player_' + str(card) + '.txt')
        card += 1

    # закрывает zip файл
    game_zip.close()
