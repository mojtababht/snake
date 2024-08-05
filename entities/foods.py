import random


class Food:

    def __init__(self):
        self.point = (random.randint(0, 14), random.randint(0, 14))


class Apple(Food):
    def __init__(self):
        super().__init__()
        self.color = 'red'


class Pineapple(Food):
    def __init__(self):
        super().__init__()
        self.color = 'yellow'
