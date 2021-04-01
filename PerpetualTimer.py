from threading import Timer, Thread, Event


class PerpetualTimer:

    def __init__(self, seconds, handler):
        self.seconds = seconds
        self.handler = handler
        self.thread = Timer(self.seconds, self.handle_function)

    def handle_function(self):
        self.handler()
        self.thread = Timer(self.seconds, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

# пример использование
# printer будет выполнятся каждые 5 секунд
# def printer():
#     print('ipsum lorem')
#
#
# t = PerpetualTimer(5, printer)
# t.start()
