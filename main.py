import time
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
                self.game_over()
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
        self.show_score()
        self.draw_food()
        pygame.display.update()

    def draw_tongue(self, head_rect):
        match self.snake.dir:
            case 'r':
                x = head_rect.right
                y = head_rect.center[1]
                points = (
                    (x, y + .07 * self.unit),
                    (x + .3 * self.unit, y + .07 * self.unit),
                    (x + .2 * self.unit, y),
                    (x + .3 * self.unit, y - .07 * self.unit),
                    (x, y - .07 * self.unit),
                )
            case 'l':
                x = head_rect.left
                y = head_rect.center[1]
                points = (
                    (x, y + .07 * self.unit),
                    (x - .3 * self.unit, y + .07 * self.unit),
                    (x - .2 * self.unit, y),
                    (x - .3 * self.unit, y - .07 * self.unit),
                    (x, y - .07 * self.unit),
                )
            case 'u':
                x = head_rect.center[0]
                y = head_rect.top
                points = (
                    (x + .07 * self.unit, y),
                    (x + .07 * self.unit, y - .3 * self.unit),
                    (x, y - .2 * self.unit),
                    (x - .07 * self.unit, y - .3 * self.unit),
                    (x - .07 * self.unit, y),
                )
            case 'd':
                x = head_rect.center[0]
                y = head_rect.bottom
                points = (
                    (x + .07 * self.unit, y),
                    (x + .07 * self.unit, y + .3 * self.unit),
                    (x, y + .2 * self.unit),
                    (x - .07 * self.unit, y + .3 * self.unit),
                    (x - .07 * self.unit, y),
                )
            case _:
                raise ValueError('snake.dir most be in ("r", "l", "u", "d")')

        pygame.draw.polygon(self.screen, 'red', points)

    def draw_head(self):
        head_rect = pygame.Rect(0, 0, .9 * self.unit, .9 * self.unit)
        head_rect.center = self.get_point_cord(self.snake.points[-1])
        pygame.draw.rect(self.screen, self.snake.color, head_rect)
        self.draw_tongue(head_rect)

    def draw_tail(self):
        tail_rect = pygame.Rect(0, 0, .9 * self.unit, .9 * self.unit)
        tail_rect.center = self.get_point_cord(self.snake.points[0])
        pygame.draw.rect(self.screen, self.snake.color, tail_rect)

    def draw_snake(self):
        points = self.snake.points
        self.draw_head()
        self.draw_tail()
        for point in points[1:-1]:
            rect = pygame.Rect(0, 0, .9 * self.unit, .9 * self.unit)
            rect.center = self.get_point_cord(point)
            pygame.draw.rect(self.screen, self.snake.color, rect)
            # filling among 2 rects
            x, y = point
            x_2, y_2 = points[points.index(point) - 1]
            if abs(x - x_2) <= 1 and abs(y - y_2) <= 1:
                rect_2 = pygame.Rect(0, 0, .9 * self.unit, .9 * self.unit)
                among_point = ((x + x_2) / 2, (y + y_2) / 2)
                rect_2.center = self.get_point_cord(among_point)
                pygame.draw.rect(self.screen, self.snake.color, rect_2)

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

    def show_score(self, color='black', font='times new roman', size=20):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        self.screen.blit(score_surface, score_rect)

    def game_over(self):
        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Your Score is : ' + str(self.score), True, 'red')
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.unit / 2, self.unit / 4)
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        quit()


if __name__ == '__main__':
    UNIT = 40
    game = Game(UNIT)
    game.main_loop()
