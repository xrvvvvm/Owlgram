from abc import ABC


class User(ABC):

    def __init__(self, name, age, avatar):
        self.name = name
        self.age = age
        self.avatar = avatar
