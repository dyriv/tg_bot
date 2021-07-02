# генерация карты игрока
from pathlib import Path
from random import choice, randint
from itertools import chain
from bunker import cleaner


# ВАЖНО!!!
# если запускать код с этого же файла нужно в начало каждого пути дописать ../ (шаг назад на одну директорию)
# если запускать код с файла bot_main.py - ничего дописывать не надо :)


# генерируем карту игрока
def get_card():
    global pl_card

    cleaner.clear_single_card()

    pl_dir = 'src/player/'

    sex = choice(('Мужчина', 'Женщина'))  # рандомим пол
    age = choice(range(18, 100))  # рандомим возраст
    exp = age // randint(6, 9)  # рандомим стаж

    # решаем как правильно написать: год/лет/года
    exp_years = 'лет'  # (стаж работы)
    if exp == 1:
        exp_years = 'год'
    elif exp in range(2, 5):
        exp_years = 'года'

    years = 'год'  # (количество лет у персонажа)
    if age in chain(range(18, 21), range(25, 31), range(35, 41), range(45, 51),
                    range(55, 61), range(65, 71), range(75, 81), range(85, 91),
                    range(95, 100)):
        years = 'лет'
    elif age in chain(range(22, 25), range(32, 35), range(42, 45), range(52, 55),
                      range(62, 65), range(72, 75), range(82, 85), range(92, 95)):
        years = 'года'

    # генерируем телосложение персонажа
    weight, height = randint(450, 1400) / 10, randint(15, 21) / 10
    bmi = weight / (height ** 2)

    if bmi <= 18:
        physique = 'Анорексия'
    elif bmi > 18 and bmi <= 18.4:
        physique = 'Недостаточный вес'
    elif bmi > 18.4 and bmi <= 24.9:
        physique = 'Нормальный вес'
    elif bmi > 24.9 and bmi <= 29.9:
        physique = 'Лишний вес'
    else:
        physique = 'Ожирение'

    pl_card = []  # карта игрока в виде списка (пока пуская)
    headlines = [
        'Пол и возраст', 'Профессия', 'Здоровье', 'Телосложение',
        'Фобия', 'Характер', 'Хобби', 'Багаж',
        'Дополнительная информация', 'Карта действия'
    ]  # даный список поможет записать характеристики персонажа в карту игрока

    i = 0
    for char in Path(pl_dir).glob('*'):  # добавляем по одной характеристике из каждого файла
        if char.is_file():
            # открываем, читаем, убираем \n с каждого файла в pl_dir
            char_list = [line.rstrip() for line in open(str(char), encoding='utf-8').readlines()]
            # вручную добавляем характеристики персонажа в карту игрока
            if i == 0:
                pl_card.append(f'{headlines[i]}: {sex} - {age} {years}\n')  # пол и возраст
                pl_card.append(f'{headlines[i + 1]}: {choice(char_list)}')  # профессию
                pl_card.append(f' | Стаж работы: {exp} {exp_years}\n')  # стаж
                i += 2
            elif i == 2:
                pl_card.append(f'{headlines[i]}: {choice(char_list)}\n')  # здоровье
                pl_card.append(
                    f'{headlines[i + 1]}: {physique} | Рост: {height} м. Вес: {weight} кг.\n')  # телосложение
                i += 2
            else:
                # автоматически добавляем характеристики которые не нужно редактировать
                pl_card.append(f'{headlines[i]}: {choice(char_list)}\n')
                i += 1


# срабатывает когда пользователь нажимает на "Карта игрока"
def single_card():
    global pl_card

    cleaner.clear_single_card()

    get_card()

    with open('files/player_card.txt', 'w', encoding='utf-8') as file:
        file.write(f''' - - - Карта игрока - - - \n{''.join(pl_card)}''')


# записуем все карты игроков в файлы
def write_card(max_pl):
    global pl_card

    cleaner.clear_card()

    player_list = range(1, (int(max_pl) + 1))  # количество играков

    first_rel = sec_rel = 0

    for player in player_list:

        get_card()  # для каждого игрока запускаем код генерирующий карту характеристик

        relative = ''
        # генерируем родство
        while first_rel == sec_rel:
            first_rel = randint(1, player_list[-1])
            sec_rel = randint(1, player_list[-1])

        if player == first_rel:
            relative = f'Игрок под номером "{sec_rel}" ваш родственник\n'
        if player == sec_rel:
            relative = f'Игрок под номером "{first_rel}" ваш родственник\n'

        with open('files/players/player_' + str(player) + '.txt', 'w', encoding='utf-8') as file:
            file.write(f''' - - - Карта игрока #{str(player)} - - - \n{''.join(pl_card)}{relative}''')

# write_card()
