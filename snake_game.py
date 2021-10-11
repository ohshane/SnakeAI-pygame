from snake import *
from misc import *
from settings import settings
from pathlib import Path
import os
import pygame


SPEED = 10000

pygame.init()
font = pygame.font.SysFont('arial', 20)

population_path = Path(os.path.abspath(__file__)).parent / 'population'
individual_path = Path(population_path / 'gen_494')
snake = load_snake(population_path, individual_path, settings)

class Size:
    BLOCK_SIZE = 20

class Color:
    BACKGROUND = (127, 215,  70)
    GRASS      = (167, 209,  61)
    APPLE      = (200,   0,   0)
    SNAKE      = (  0, 100, 255)
    SNAKE_HEAD_BORDER = (  0,  0,  0)
    SNAKE_BODY_BORDER = (  0,  0,255)

class Vision(object):
    __slots__ = ('dist_to_wall', 'dist_to_apple', 'dist_to_self')
    def __init__(self,
                 dist_to_wall: Union[float, int],
                 dist_to_apple: Union[float, int],
                 dist_to_self: Union[float, int]
                 ):
        self.dist_to_wall = float(dist_to_wall)
        self.dist_to_apple = float(dist_to_apple)
        self.dist_to_self = float(dist_to_self)

class DrawableVision(object):
    __slots__ = ('wall_location', 'apple_location', 'self_location')
    def __init__(self,
                wall_location: Point,
                apple_location: Optional[Point] = None,
                self_location: Optional[Point] = None,
                ):
        self.wall_location = wall_location
        self.apple_location = apple_location
        self.self_location = self_location

class SnakeGame:
    def __init__(self, snake=snake, visible=True, speed=SPEED):
        self.snake = snake
        self.visible = visible
        self.speed = speed
        self.screen = pygame.display.set_mode(tuple(map(lambda x: x*Size.BLOCK_SIZE, self.snake.board_size)))
        self.clock = pygame.time.Clock()
    
    def play_scene(self):
        if self.snake.is_alive:
            self.snake.move()
            self.snake.update()
        else: # dead
            pass
        if self.visible:
            self.render()
            self.clock.tick(self.speed)
        is_game_over = not self.snake.is_alive
        return is_game_over, self.snake.score

    def render(self):
        self.__render_background()
        self.__render_snake()
        self.__render_apple()
        self.screen.blit(
            font.render(f'Score: {self.snake.score}', True, (0,0,0)),
            (0,0)
        )
        pygame.display.update()

    def __render_background(self):
        self.screen.fill(Color.BACKGROUND)
        for x in range(self.snake.board_size[0]):
            for y in range(self.snake.board_size[1]):
                if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 != 0):
                    self.__render_block(Point(x,y), Color.GRASS)

    def __render_snake(self):
        for i, point in enumerate(self.snake.snake_array):
            if i == 0: self.__render_border_block(point, Color.SNAKE, Color.SNAKE_HEAD_BORDER)
            else: self.__render_border_block(point, Color.SNAKE, Color.SNAKE_BODY_BORDER)

    def __render_apple(self):
        self.__render_block(self.snake.apple_location, Color.APPLE)
    
    def __render_border_block(self, point: Point, color, border_color, border_size=4):
        self.__render_block(point, border_color)
        self.__render_block(point, color, padding=border_size)
    
    def __render_block(self, point: Point, color, padding=0):
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(
                Size.BLOCK_SIZE*point.x + padding,
                Size.BLOCK_SIZE*point.y + padding,
                Size.BLOCK_SIZE - 2*padding,
                Size.BLOCK_SIZE - 2*padding
            ))

if __name__ == '__main__':
    game = SnakeGame()
    while True:
        is_game_over, score = game.play_scene()
        if is_game_over:
            print(is_game_over, score)
            break