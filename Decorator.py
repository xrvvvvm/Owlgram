from abc import ABC, abstractmethod


class Notifier(ABC):

    @abstractmethod
    def send(self):
        pass


class ConcreteNotifier(Notifier):

    def send(self):
        return 'Уведомление: '


class BaseDecorator(Notifier):

    _notify = None

    def __init__(self, notify):
        self._notify = notify

    def send(self):
        self._notify.send()


class InsideNetworkDecorator(BaseDecorator):

    def send(self):
        return self._notify.send() + '\nОтправлено внутри сети'


class OnEmailDecorator(BaseDecorator):

    def send(self):
        return self._notify.send() + '\nОтправлено по email'


class OnTelegramDecorator(BaseDecorator):

    def send(self):
        return self._notify.send() + '\nОтправлено в telegram'


class OnWhatsAppDecorator(BaseDecorator):

    def send(self):
        return self._notify.send() + '\nОтправлено в whats app'


class OnViberDecorator(BaseDecorator):

    def send(self):
        return self._notify.send() + '\nОтправлено в viber'




