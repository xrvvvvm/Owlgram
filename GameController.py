import Roles
import Post
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


def print_owl_actions():
    """
    Выводит действия для совы
    """
    print('1 - Выложить пост', '2 - Проверить лайки подписчиков',
          '3 - Мои характеристики', '4 - Выйти', sep='\n')


def show_owl_posts(owl):
    """
    Показывает посты совы
    """
    i = 0
    for post in owl.posts:
        print(f'{i} \t {post.message} \t {post.photo} \t {post.geotag}')
        i += 1


def send_post(owl):
    """
    Отправляет пост
    """
    print('Введите подпись: ', end=' ')
    message = input()
    print('Загрузите фото: ', end=' ')
    photo = input()
    print('Поставьте геометку: ', end=' ')
    geotag = input()
    post = Post.Post(message, geotag, photo)
    owl.post(post)


def check_likes(owl):
    """
    Проверяет, кто не лайкнул посты, и съедает мышь, которая не лайкнула n последних постов
    """
    posts = list(reversed(owl.posts))
    prev_unliked_mice = owl.observers
    n = 3 if len(posts) >= 3 else len(posts)
    for i in range(0, n):
        # находит мышей, которые не лайкнули текущий пост
        unliked_mice = subtract_lists(owl.observers, posts[i].liked)
        # сохраняет мышей, которые не лайкнули предыдущий пост
        prev_unliked_mice = intersection_lists(prev_unliked_mice, unliked_mice)
    for mouse in prev_unliked_mice:
        owl.eat_mouse(mouse)
        mice.remove(mouse)
    print(f'Съедено {len(prev_unliked_mice)} мышей')


def show_owl_info(owl):
    """
    Показывает уровень счастья и сытости совы
    """
    print('Уровень счастья:', owl.happiness_lvl)
    print('Уровень сытости:', owl.satiety_lvl)


def enter_owl(owl):
    """
    Вход за сову
    """
    while True:
        print_owl_actions()
        choice = input()
        if choice == '1':
            send_post(owl)
        elif choice == '2':
            check_likes(owl)
        elif choice == '3':
            show_owl_info(owl)
        elif choice == '4':
            main_actions()
        else:
            print('Введите крректную команду')


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
                enter_owl(i)
            else:
                print('Неправильный пароль')
    for i in mice:
        if i.name == name:
            if i.password == password:
                i.enter_mouse()
            else:
                print('Неправильный пароль')
    print('Такого пользователя не существует')
    main_actions()


def create_new_user(name, age, avatar, password):
    """
    Создает нового пользователя и присваивает ему роль
    """
    rand = random.random()
    if rand > 0.7:
        return Roles.Owl(name, age, avatar, password)
    else:
        return Roles.Mouse(name, age, avatar, password)


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
    if isinstance(new_user, Roles.Mouse):
        mice.append(new_user)
        # enter_mouse(new_user)
        new_user.enter_mouse()
    else:
        owls.append(new_user)
        enter_owl(new_user)


def main_actions():
    """
    Выводит действия неавторизированного пользователя
    """
    while True:
        print_main_actions()
        choice = input()
        if choice == '1':
            register()
        elif choice == '2':
            enter()
        else:
            print('Введите крректную команду')


def start():
    """
    Запуск соц. сети
    """
    mouse_timer.start()
    owl_timer.start()
    main_actions()