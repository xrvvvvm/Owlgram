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
        print(f'{owl.name} \t {owl.happiness_lvl} \t {owl.satiety_lvl}')
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


def print_mouse_actions():
    """
    Выводит действия для мыши
    """
    print('1 - Подписки', '2 - Последние посты', '3 - Моё время жизни',
          '4 - Просмотр остальных сов', '5 - Способ получения уведомлений', '6 - Выйти', sep='\n')


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


def print_mouse_subscriptions(mouse):
    """
    Выводит подписки мыши
    """
    i = 1
    for owl in mouse.subscriptions:
        print(f'{i} \t {owl.name} \t {owl.avatar}; \t \t "{i} 0" - отписаться; "{i} 1" - посмотреть посты')
        i += 1


def show_subscriptions(mouse):
    """
    Показывает сов, на которых подписана мышь
    """
    print_mouse_subscriptions(mouse)
    while 1:
        print('Введите действие напротив совы или "q", чтобы вернуться')
        choice = input().split(' ')
        if choice[0] == 'q':
            enter_mouse(mouse)
        # не будет работать, если сов будет больше 9 ???
        if len(choice) < 2:
            print('Введите корректную команду')
            continue
        owl_idx = int(choice[0])
        if 0 <= owl_idx < len(mouse.subscriptions):
            if int(choice[1]) == 0:
                mouse.unsubscribe(mouse.subscriptions[owl_idx])
                print(f'Вы отписались от {mouse.subscriptions[owl_idx].name}')
                print_mouse_subscriptions(mouse)
            elif int(choice[1]) == 1:
                show_owl_posts(mouse.subscriptions[owl_idx])
        else:
            print('Введите корректную команду')
            continue


def show_unliked_posts(mouse):
    """
    Показывает посты, которые мышь не лайкнула
    """
    i = 0
    posts = []
    for owl in mouse.subscriptions:
        print(f'{owl.name}:')
        for post in owl.posts:
            try:
                contain = post.liked.index(mouse)
            except ValueError:
                print(f'{i} \t {post.message} \t {post.photo} \t {post.geotag}; "{i} 0" - лайкнуть')
                posts.append(post)
                i += 1
    while 1:
        print('Введите действие напротив поста или "q", чтобы вернуться')
        choice = input().split(' ')
        if choice[0] == 'q':
            enter_mouse(mouse)
        if len(choice) < 2:
            print('Введите корректную команду')
            continue
        if 0 <= int(choice[0]) <= i:
            if int(choice[1]) == 0:
                posts[i - 1].like(mouse)
                print(f'Вы лайкнули пост {i - 1}')
        else:
            print('Введите корректную команду')
            continue


def show_mouse_info(mouse):
    """
    Показывает время жизни мыши
    """
    print('Время жизни:', mouse.life_time)


def show_other_owls(mouse):
    """
    Показывает сов, на которых мышь не подписана
    """
    i = 0
    no_subs_owls = []
    for owl in owls:
        try:
            contain = owl.observers.index(mouse)
        except ValueError:
            print(f'{i} \t {owl.name} \t {owl.avatar}; \t \t "{i} 0" - подписаться; "{i} 1" - посмотреть посты')
            no_subs_owls.append(owl)
            i += 1
    while 1:
        print('Введите действие напротив совы или "q", чтобы вернуться')
        # print(f'*** i = {i}')
        choice = input().split()
        if choice[0] == 'q':
            enter_mouse(mouse)
        if len(choice) < 2:
            print('Введите корректную команду')
            continue
        owl_idx = int(choice[0])
        if 0 <= owl_idx <= i:
            # print(f'*** int(choice[0]) = {owl_idx}')
            if int(choice[1]) == 0:
                mouse.subscribe(no_subs_owls[owl_idx])
                print(f'Вы подписались на {no_subs_owls[owl_idx].name}')
            elif int(choice[1]) == 1:
                show_owl_posts(no_subs_owls[owl_idx])
        else:
            print('Введите корректную команду')
            continue


def print_notifications_methods(mouse):
    if mouse.notify_inside_network:
        print('Уведомления внутри сети подключены')
    else:
        print('Уведомления внутри сети отключены. "1" - подключить')

    if mouse.notify_email:
        print('Уведомления по email подключены')
    else:
        print('Уведомления по email отключены. "2" - подключить')

    if mouse.notify_telegram:
        print('Уведомления в telegram подключены')
    else:
        print('Уведомления в telegram отключены. "3" - подключить')

    if mouse.notify_whats_app:
        print('Уведомления в whats app подключены')
    else:
        print('Уведомления в whats app отключены. "4" - подключить')

    if mouse.notify_viber:
        print('Уведомления в viber подключены')
    else:
        print('Уведомления в viber отключены. "5" - подключить')

    print('"q" - назад')


def select_notification_methods(mouse):
    """
    Устанавлевает способы уведомления
    """
    while 1:
        print_notifications_methods(mouse)
        choice = input()
        if choice == '1':
            mouse.notification_inside_network_on()
        elif choice == '2':
            mouse.notification_email_on()
        elif choice == '3':
            mouse.notification_telegram_on()
        elif choice == '4':
            mouse.notification_whats_app_on()
        elif choice == '5':
            mouse.notification_viber_on()
        elif choice == 'q':
            enter_mouse(mouse)
        else:
            print('Введите крректную команду')


def enter_mouse(mouse):
    """
    Вход за мышь
    """
    while 1:
        print_mouse_actions()
        choice = input()
        if choice == '1':
            show_subscriptions(mouse)
        elif choice == '2':
            show_unliked_posts(mouse)
        elif choice == '3':
            show_mouse_info(mouse)
        elif choice == '4':
            show_other_owls(mouse)
        elif choice == '5':
            select_notification_methods(mouse)
        elif choice == '6':
            main_actions()
        else:
            print('Введите крректную команду')


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
    # posts = owl.posts.reverse()
    posts = list(reversed(owl.posts))
    prev_unliked_mice = owl.observers
    # print(posts)
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
    while 1:
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
                enter_mouse(i)
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
        enter_mouse(new_user)
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

