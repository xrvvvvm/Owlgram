from abc import ABC, abstractmethod


class Notifier(ABC):

    @abstractmethod
    def send(self):
        pass


class ConcreteNotifier(Notifier):

    def send(self):
        return 'Notifier: '


class BaseDecorator(Notifier):

    _notify = None

    def __init__(self, notify):
        self._notify = notify

    def send(self):
        self._notify.send()


class InsideNetworkDecorator(BaseDecorator):

    def send(self):
        return self._notify.send() + 'The notification was sent to inside network'


class OnEmailDecorator(BaseDecorator):

    def send(self):
        return self._notify.send() + 'The notification was sent to email'


class OnTelegramDecorator(BaseDecorator):

    def send(self):
        return self._notify.send() + '\nThe notification was sent to Telegram'


class OnWhatsAppDecorator(BaseDecorator):

    def send(self):
        return self._notify.send() + '\nThe notification was sent to WhatsApp'


class OnViberDecorator(BaseDecorator):

    def send(self):
        return self._notify.send() + '\nThe notification was sent to Viber'




