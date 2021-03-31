from Observer import Subject, Observer
import User
import Decorator


class Owl(Subject, User):
    _posts = []
    _observers = []

    _happiness_lvl = 100
    _satiety_lvl = 50

    def __init__(self, name, age, avatar):
        super().__init__(name, age, avatar)

    def attach(self, observer):
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def post(self):
        print("\nSubject: I'm doing something important.")
        # self._state = randrange(0, 10)

        print(f"Subject: My state has just changed to: {self}")
        self.notify()

    def happiness_up(self):
        self._happiness_lvl += 1

    def satiety_up(self):
        self._satiety_lvl += 1

    def happiness_down(self):
        self._happiness_lvl -= 1

    def satiety_down(self):
        self._satiety_lvl -= 1


class Mouse(Observer, User):

    _life_time = 0
    _notifier = Decorator.ConcreteNotifier()

    def __init__(self, name, age, avatar):
        super().__init__(name, age, avatar)

    def update(self, subject):
        pass

    def life_time_up(self):
        self._life_time += 1

    def get_notification_inside_network(self):
        self._notifier = Decorator.InsideNetworkDecorator(self._notifier)

    def get_notification_on_email(self):
        self._notifier = Decorator.OnEmailDecorator(self._notifier)

    def get_notification_on_telegram(self):
        self._notifier = Decorator.OnTelegramDecorator(self._notifier)

    def get_notification_on_viber(self):
        self._notifier = Decorator.OnViberDecorator(self._notifier)

    def get_notification_on_whatsapp(self):
        self._notifier = Decorator.OnWhatsAppDecorator(self._notifier)


