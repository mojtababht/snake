import pygame

from entities.snake import Snake
from entities.foods import Apple, Pineapple


class Game:
    bg_color = (162, 209, 73)

    def __init__(self, unit):
        self.tick = 0
        self.score = 0
        self.eaten_apple = 0
        pygame.init()
        self.unit = unit
        screen_size = unit * 15
        self.screen = pygame.display.set_mode((screen_size, screen_size))
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = self.get_food()
        self.update()
        self.clock.tick(5)

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                running = self.handel_event(event)
            pygame.display.flip()
            if not self.move():
                print(f'game over! your score is: {self.score}')
                running = False
            self.clock.tick(5)
            if type(self.food) == Pineapple:
                if self.tick == 30:
                    self.food = self.get_food(True)
                    self.tick = 0
                else:
                    self.tick += 1
        pygame.quit()

    def handel_event(self, event):
        match event.type:
            case pygame.QUIT:
                return False
            # case pygame.MOUSEBUTTONDOWN:
            #     print(event.pos)
            #     return True
            case pygame.KEYDOWN:
                self.snake.change_dir(pygame.key.name(event.key)[0])
                return True
            case _:
                return True

    def update(self):
        self.screen.fill(self.bg_color)
        self.draw_snake()
        self.draw_food()
        pygame.display.update()

    def draw_snake(self):
        points = self.snake.points
        for point in points:
            rect = pygame.Rect(0, 0, self.unit, self.unit)
            rect.center = self.get_point_cord(point)
            pygame.draw.rect(self.screen, self.snake.color, rect)
        # head_rect = pygame.Rect(0, 0, self.unit, self.unit)
        # head_x, head_y = self.get_point_cord(points[-1])
        # head_rect.center = head_x, head_y
        # pygame.draw.ellipse(self.screen, snake.color, head_rect)
        # b_head_x, b_head_y = self.get_point_cord(points[-2])
        # mid_rect = pygame.Rect(0, 0, self.unit, self.unit)
        # mid_rect.center = (b_head_x + head_x) / 2, (b_head_y + head_y) / 2
        # pygame.draw.rect(self.screen, self.snake.color, mid_rect)

    def draw_apple(self):
        rect = pygame.Rect(0, 0, self.unit, self.unit)
        rect.center = self.get_point_cord(self.food.point)
        pygame.draw.rect(self.screen, self.food.color, rect)
        pygame.display.update()

    def draw_pineapple(self):
        rect = pygame.Rect(0, 0, self.unit, self.unit)
        rect.center = self.get_point_cord(self.food.point)
        pygame.draw.rect(self.screen, self.food.color, rect)
        pygame.display.update()

    def get_point_cord(self, point):
        x, y = point
        x = (self.unit / 2) + (x * self.unit)
        y = (self.unit / 2) + (y * self.unit)
        return x, y

    def move(self):
        new_point = self.snake.move(self.food.point)
        if self.snake.points.count(new_point) >= 2:
            return False
        if new_point == self.food.point:
            if type(self.food) == Apple:
                self.score += 1
                self.eaten_apple += 1
            elif type(self.food) == Pineapple:
                self.score += 5
            self.food = self.get_food(type(self.food) == Pineapple)
        self.update()
        return True

    def get_food(self, reset=False):
        if not reset and self.eaten_apple != 0 and self.eaten_apple % 5 == 0:
            food_class = Pineapple
            self.tick = 0
        else:
            food_class = Apple
        food = food_class()
        while food.point in self.snake.points:
            food = food_class()
        return food

    def draw_food(self):
        if type(self.food) == Apple:
            self.draw_apple()
        else:
            self.draw_pineapple()


if __name__ == '__main__':
    UNIT = 40
    game = Game(UNIT)
    game.main_loop()
