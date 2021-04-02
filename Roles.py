from Observer import Subject, Observer
import Decorator


class Owl(Subject):
    def __init__(self, name, age, avatar, password):
        self.name = name
        self.age = age
        self.avatar = avatar
        self.password = password
        self.posts = []
        self.observers = []
        self.dead = False
        self.happiness_lvl = 50
        self.satiety_lvl = 100

    @property
    def dead(self):
        return self.__dead

    @dead.setter
    def dead(self, dead):
        self.__dead = dead

    @property
    def happiness_lvl(self):
        return self.__happiness_lvl

    @happiness_lvl.setter
    def happiness_lvl(self, happiness_lvl):
        self.__happiness_lvl = happiness_lvl

    @property
    def satiety_lvl(self):
        return self.__satiety_lvl

    @satiety_lvl.setter
    def satiety_lvl(self, satiety_lvl):
        self.__satiety_lvl = satiety_lvl

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, post):
        for observer in self.observers:
            observer.update(self, post)

    def post(self, post):
        self.posts.append(post)
        print('Пост опубликован')
        self.happiness_up()
        print(f'Уровень счастья: {self.happiness_lvl}')
        self.notify(post)

    def eat_mouse(self, mouse):
        self.observers.remove(mouse)
        mouse.dead = True
        print(f'{mouse.name} съедена')
        self.satiety_up()
        print(f'Уровень сытости: {self.satiety_lvl}')

    def happiness_up(self):
        self.happiness_lvl += 1

    def satiety_up(self):
        self.satiety_lvl += 1

    def happiness_down(self):
        self.happiness_lvl -= 1
        if self.happiness_lvl <= 0:
            self.dead = True

    def satiety_down(self):
        self.satiety_lvl -= 1
        if self.satiety_lvl <= 0:
            self.dead = True


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
