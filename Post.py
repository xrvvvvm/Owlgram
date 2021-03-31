class Post:

    def __init__(self, message, geotag, photo):
        self.__message = message
        self.__geotag = geotag
        self.__photo = photo
        self.__liked = []

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message

    @property
    def geotag(self):
        return self.__geotag

    @geotag.setter
    def geotag(self, geotag):
        self.__geotag = geotag

    @property
    def photo(self):
        return self.__photo

    @photo.setter
    def photo(self, photo):
        self.__photo = photo

    @property
    def liked(self):
        return self.__liked

    def like(self, liked_mouse):
        if liked_mouse not in self.__liked:
            self.liked.append(liked_mouse)

    def remove_like(self, liked_mouse):
        if liked_mouse in self.__liked:
            self.liked.remove(liked_mouse)
