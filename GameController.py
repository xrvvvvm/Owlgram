from Owl import Owl
from Mouse import Mouse
from PerpetualTimer import PerpetualTimer
import random
import getpass

owls = []
mice = []


def mouse_timer_tick():
    """
    Прибавляет время жизни мышей
    """
    for mouse in mice:
        mouse.life_time_up()
        # print(f'Мышь {mouse.name} прожила {mouse.life_time}')


def owl_timer_tick():
    """
    Понижает уровень счастья и сытости у сов
    """
    for owl in owls:
        owl.happiness_down()
        owl.satiety_down()
        # print(f'{owl.name} \t {owl.happiness_lvl} \t {owl.satiety_lvl}')
        if owl.dead:
            owls.remove(owl)
            print(f'Сова {owl.name} мертва')


owl_timer = PerpetualTimer(30, owl_timer_tick)
mouse_timer = PerpetualTimer(1, mouse_timer_tick)


def intersection_lists(l1, l2):
    """
    Возвращает пересечение списков l1 & l2
    """
    result = []
    for i in l1:
        for j in l2:
            if i == j:
                result.append(i)
    return result


def subtract_lists(l1, l2):
    """
    Возвращает разность списков l1 - l2
    """
    result = []
    for i in l1:
        no_contains = True
        for j in l2:
            if i == j:
                no_contains = False
                break
        if no_contains:
            result.append(i)
    return result


def print_main_actions():
    """
    Выводит действия при включении соц. сети
    """
    print('1 - Зарегистрироваться', '2 - Войти', sep='\n')


def enter():
    """
    Вход за существующего пользователя
    """
    print('Введите имя (логин): ', end=' ')
    name = input()
    print('Введите пароль: ', end=' ')
    password = getpass.getpass()
    for i in owls:
        if i.name == name:
            if i.password == password:
                i.enter_owl()
            else:
                print('Неправильный пароль')
        else:
            print('Такого пользователя не существует')
    for i in mice:
        if i.name == name:
            if i.password == password:
                i.enter_mouse()
            else:
                print('Неправильный пароль')
        else:
            print('Такого пользователя не существует')
    main_actions()


def create_new_user(name, age, avatar, password):
    """
    Создает нового пользователя и присваивает ему роль
    """
    rand = random.random()
    if rand > 0.7:
        return Owl(name, age, avatar, password)
    else:
        return Mouse(name, age, avatar, password)


def register():
    """
    Регистрация нового пользователя
    """
    print('Введите имя (логин): ', end=' ')
    name = input()
    print('Введите возраст: ', end=' ')
    age = input()
    print('Загрузите аватар: ', end=' ')
    avatar = input()
    print('Введите пароль: ', end=' ')
    password = getpass.getpass('')
    new_user = create_new_user(name, age, avatar, password)
    if isinstance(new_user, Mouse):
        mice.append(new_user)
        new_user.enter_mouse()
    else:
        owls.append(new_user)
        Owl.enter_owl(new_user)


def main_actions():
    """
    Выводит действия неавторизированного пользователя
    """
    while True:
        print_main_actions()
        choice = input()
        number_act = {
            '1': register,
            '2': enter
        }
        number_act[choice]() if choice in number_act else print('Введите корректную команду')


def start():
    """
    Запуск соц. сети
    """
    mouse_timer.start()
    owl_timer.start()
    main_actions()
