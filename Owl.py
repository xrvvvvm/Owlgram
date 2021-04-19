from Observer import Subject
import Decorator
import GameController
from Post import Post


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

    def show_owl_posts(self):
        """
        Показывает посты совы
        """
        i = 0
        for post in self.posts:
            print(f'{i} \t {post.message} \t {post.photo} \t {post.geotag}')
            i += 1

    def print_owl_actions(self):
        """
        Выводит действия для совы
        """
        print('1 - Выложить пост', '2 - Проверить лайки подписчиков',
              '3 - Мои характеристики', '4 - Выйти', sep='\n')

    def send_post(self):
        """
        Отправляет пост
        """
        print('Введите подпись: ', end=' ')
        message = input()
        print('Загрузите фото: ', end=' ')
        photo = input()
        print('Поставьте геометку: ', end=' ')
        geotag = input()
        post = Post(message, geotag, photo)
        self.post(post)

    def check_likes(self):
        """
        Проверяет, кто не лайкнул посты, и съедает мышь, которая не лайкнула n последних постов
        """
        posts = list(reversed(self.posts))
        prev_unliked_mice = self.observers
        n = 3 if len(posts) >= 3 else len(posts)
        for i in range(0, n):
            # находит мышей, которые не лайкнули текущий пост
            unliked_mice = GameController.subtract_lists(self.observers, posts[i].liked)
            # сохраняет мышей, которые не лайкнули предыдущий пост
            prev_unliked_mice = GameController.intersection_lists(prev_unliked_mice, unliked_mice)
        for mouse in prev_unliked_mice:
            self.eat_mouse(mouse)
            GameController.mice.remove(mouse)
        print(f'Съедено {len(prev_unliked_mice)} мышей')

    def show_owl_info(self):
        """
        Показывает уровень счастья и сытости совы
        """
        print('Уровень счастья:', self.happiness_lvl)
        print('Уровень сытости:', self.satiety_lvl)

    def enter_owl(self):
        """
        Вход за сову
        """
        while True:
            self.print_owl_actions()
            choice = input()
            if choice == '1':
                self.send_post()
            elif choice == '2':
                self.check_likes()
            elif choice == '3':
                self.show_owl_info()
            elif choice == '4':
                GameController.main_actions()
            else:
                print('Введите крректную команду')
