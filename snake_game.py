from snake import *
from misc import *
from settings import settings
from pathlib import Path
import os
import pygame


SPEED = 100
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
    def __init__(self, *, individual_name='gen_1040', visible=True, speed=SPEED):
        population_path = Path(os.path.abspath(__file__)).parent / 'population'
        self.snake = load_snake(population_path, individual_name, settings)
        self.visible = visible
        self.speed = speed
        self.game_over = False

        if self.visible:
            pygame.init()
            self.screen = pygame.display.set_mode(tuple(map(lambda x: x*Size.BLOCK_SIZE, self.snake.board_size)))
        self.clock = pygame.time.Clock()
    
    def play_scene(self):
        if self.game_over:
            pygame.quit()
        else:
            if self.visible:
                self.render()

            self.snake.update()
            self.game_over = not self.snake.move()
            
            self.clock.tick(self.speed)
        return self.game_over, self.snake.score

    def render(self):
        self.__render_background()
        self.__render_snake()
        self.__render_apple()

        font = pygame.font.SysFont('arial', 20)
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
    import matplotlib.pyplot as plt
    import numpy as np

    test_size = (10,10)

    print(f'{f" test {test_size} ":=^30}')

    board_size = None
    scores = []
    for i in range(test_size[0]):
        temp_scores = []
        for j in range(test_size[1]):
            game = SnakeGame(individual_name='gen_1493', visible=False, speed=np.inf)
            perfect = game.snake.board_size[0]*game.snake.board_size[1] - 3
            if board_size is None:
                board_size = game.snake.board_size
            while True:
                is_game_over, score = game.play_scene()
                print(f'{f"iter_{i+1}_{j+1}":<15} {f"{score:>6.1f}/{perfect}":>10} {score*100/perfect:>6.2f}%', end='\r')
                if is_game_over:
                    temp_scores.append(score)
                    break
        print(f'{f"iter_{i+1}":<15} {f"{np.mean(temp_scores):>6.1f}/{perfect}":>10} {np.mean(temp_scores)*100/perfect:>6.2f}%')
        scores.append(temp_scores)

    print('='*30)
    scores = np.transpose(np.array(scores))
    print(f'max    {np.max(scores):>7.3f}')
    print(f'mean   {np.mean(scores):>7.3f}')
    print(f'median {np.median(scores):>7.3f}')
    print(f'min    {np.min(scores):>7.3f}')

    plt.figure(figsize=(10,10))
    ax = plt.subplot()
    ax.set_title('Scores')
    ax.boxplot(scores, showmeans=True)
    plt.ylim((0, board_size[0]*board_size[1]-3))
    plt.show()