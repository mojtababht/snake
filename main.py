import pygame

from entities.snake import Snake
from entities.foods import Apple


class Game:
    bg_color = (162, 209, 73)

    def __init__(self, unit):
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
            self.move()
            self.update()
            self.clock.tick(5)
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
        self.draw_apple()
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

    def get_point_cord(self, point):
        x, y = point
        x = (self.unit / 2) + (x * self.unit)
        y = (self.unit / 2) + (y * self.unit)
        return x, y

    def move(self):
        if self.snake.move(self.food.point) == self.food.point:
            self.food = self.get_food()

    def get_food(self):
        food = Apple()
        while food.point in self.snake.points:
            food = Apple()
        return food


if __name__ == '__main__':
    UNIT = 40
    game = Game(UNIT)
    game.main_loop()
