from Observer import Observer
import Decorator
import GameController
from Owl import Owl


class Mouse(Observer):

    def __init__(self, name, age, avatar, password):
        self.name = name
        self.age = age
        self.avatar = avatar
        self.password = password
        self.subscriptions = []
        self.__life_time = 0
        self.dead = False
        self.__notifier = Decorator.ConcreteNotifier()
        self.notify_inside_network = False
        self.notify_email = False
        self.notify_telegram = False
        self.notify_whats_app = False
        self.notify_viber = False

    def update(self, subject, post):
        print(f'Мышь {self.name} уведомлена')
        notification = self.__notifier.send()
        print(notification)

    def unsubscribe(self, owl):
        self.subscriptions.remove(owl)
        owl.detach(self)

    def subscribe(self, owl):
        self.subscriptions.append(owl)
        owl.attach(self)

    @property
    def life_time(self):
        return self.__life_time

    @property
    def dead(self):
        return self.__dead

    @dead.setter
    def dead(self, dead):
        self.__dead = dead

    def life_time_up(self):
        self.__life_time += 1

    def notification_inside_network_on(self):
        self.__notifier = Decorator.InsideNetworkDecorator(self.__notifier)
        self.notify_inside_network = True

    def notification_email_on(self):
        self.__notifier = Decorator.OnEmailDecorator(self.__notifier)
        self.notify_email = True

    def notification_telegram_on(self):
        self.__notifier = Decorator.OnTelegramDecorator(self.__notifier)
        self.notify_telegram = True

    def notification_viber_on(self):
        self.__notifier = Decorator.OnViberDecorator(self.__notifier)
        self.notify_viber = True

    def notification_whats_app_on(self):
        self.__notifier = Decorator.OnWhatsAppDecorator(self.__notifier)
        self.notify_whats_app = True

    # @staticmethod
    def print_mouse_actions(self):
        """
        Выводит действия для мыши
        """
        print('1 - Подписки', '2 - Последние посты', '3 - Моё время жизни',
              '4 - Просмотр остальных сов', '5 - Способ получения уведомлений', '6 - Выйти', sep='\n')

    def print_mouse_subscriptions(self):
        """
        Выводит подписки мыши
        """
        i = 0
        for owl in self.subscriptions:
            print(f'{i} \t {owl.name} \t {owl.avatar}; \t \t "{i} 0" - отписаться; "{i} 1" - посмотреть посты')
            i += 1

    def show_subscriptions(self):
        """
        Показывает сов, на которых подписана мышь
        """
        self.print_mouse_subscriptions()
        while 1:
            print('Введите действие напротив совы или "q", чтобы вернуться')
            choice = input().split(' ')
            if choice[0] == 'q':
                self.enter_mouse()
            if len(choice) != 2:
                print('Введите корректную команду')
                continue
            try:
                owl_idx = int(choice[0])
                action = int(choice[1])
            except ValueError:
                print('Введите корректную команду')
                continue
            if 0 <= owl_idx < len(self.subscriptions):
                if action == 0:
                    self.unsubscribe(self.subscriptions[owl_idx])
                    print(f'Вы отписались от {self.subscriptions[owl_idx].name}')
                    self.print_mouse_subscriptions()
                elif action == 1:
                    Owl.show_owl_posts(self.subscriptions[owl_idx])
                else:
                    print('Введите корректную команду')
                    continue
            else:
                print('Введите корректную команду')
                continue
        return

    def show_unliked_posts(self):
        """
        Показывает посты, которые мышь не лайкнула
        """
        while 1:
            i = 0
            posts = []
            for owl in self.subscriptions:
                print(f'{owl.name}:')
                for post in owl.posts:
                    if self not in post.liked:
                        print(f'{i} \t {post.message} \t {post.photo} \t {post.geotag}; "{i} 0" - лайкнуть')
                        posts.append(post)
                        i += 1
            print('Введите действие напротив поста или "q", чтобы вернуться')
            choice = input().split(' ')
            if choice[0] == 'q':
                self.enter_mouse()
            try:
                post_idx = int(choice[0])
                action = int(choice[1])
            except ValueError or IndexError:
                print('Введите корректную команду')
                continue
            if len(choice) != 2 or post_idx > i:
                print('Введите корректную команду')
                continue
            if action == 0:
                posts[post_idx].like(self)
                print(f'Вы лайкнули пост {post_idx}')

    def show_mouse_info(self):
        """
        Показывает время жизни мыши
        """
        print('Время жизни:', self.life_time)

    def show_other_owls(self):
        """
        Показывает сов, на которых мышь не подписана
        """
        no_subs_owls = []
        while 1:
            i = 0
            # no_subs_owls = []
            for owl in GameController.owls:
                if self not in owl.observers:
                    print(f'{i} \t {owl.name} \t {owl.avatar}; \t \t "{i} 0" - подписаться; "{i} 1" - посмотреть посты')
                    no_subs_owls.append(owl)
                    i += 1
            print('Введите действие напротив совы или "q", чтобы вернуться')
            choice = input().split()
            if choice[0] == 'q':
                self.enter_mouse()
            try:
                owl_idx = int(choice[0])
                action = int(choice[1])
            except ValueError or IndexError:
                print('Введите корректную команду')
                continue
            if len(choice) != 2 or owl_idx > i:
                print('Введите корректную команду')
                continue
            if action == 0:
                self.subscribe(no_subs_owls[owl_idx])
                print(f'Вы подписались на {no_subs_owls[owl_idx].name}')
            elif action == 1:
                # вынести данную функцию в класс Post
                Owl.show_owl_posts(no_subs_owls[owl_idx])

    def print_notifications_methods(self):
        if self.notify_inside_network:
            print('Уведомления внутри сети подключены')
        else:
            print('Уведомления внутри сети отключены. "1" - подключить')

        if self.notify_email:
            print('Уведомления по email подключены')
        else:
            print('Уведомления по email отключены. "2" - подключить')

        if self.notify_telegram:
            print('Уведомления в telegram подключены')
        else:
            print('Уведомления в telegram отключены. "3" - подключить')

        if self.notify_whats_app:
            print('Уведомления в whats app подключены')
        else:
            print('Уведомления в whats app отключены. "4" - подключить')

        if self.notify_viber:
            print('Уведомления в viber подключены')
        else:
            print('Уведомления в viber отключены. "5" - подключить')

        print('"q" - назад')

    def select_notification_methods(self):
        """
        Устанавлевает способы уведомления
        """
        while 1:
            self.print_notifications_methods()
            choice = input()
            act_func = {
                '1': self.notification_inside_network_on,
                '2': self.notification_email_on,
                '3': self.notification_telegram_on,
                '4': self.notification_whats_app_on,
                '5': self.notification_viber_on,
                'q': self.enter_mouse
            }
            act_func[choice]() if choice in act_func else print('Введите корректную команду')

    def enter_mouse(self):
        while 1:
            self.print_mouse_actions()
            choice = input()
            number_act = {
                '1': self.show_subscriptions,
                '2': self.show_unliked_posts,
                '3': self.show_mouse_info,
                '4': self.show_other_owls,
                '5': self.select_notification_methods,
                '6': GameController.main_actions
            }
            number_act[choice]() if choice in number_act else print('Введите корректную команду')
