from abc import ABC, abstractmethod


class Subject(ABC):

    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self, post):
        pass


class Observer(ABC):

    @abstractmethod
    def update(self, subject, post):
        pass
