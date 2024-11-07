import pygame, sys, random
from pygame.math import Vector2

class Fruit:
    def __init__(self):
        self.randomize()
        self.color = pygame.Color('red')

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, self.color, fruit_rect)

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.color = pygame.Color('blue')
        self.direction =Vector2(-1, 0)
        self.has_new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, self.color, block_rect)
    
    def move_snake(self):
        if self.has_new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.has_new_block = False

        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.has_new_block = True

class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        print("game over")
        pygame.quit()
        sys.exit()

pygame.init()

cell_size = 40
cell_number = 20
screen_size = cell_number * cell_size

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_size, screen_size))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            game.update()

        if event.type == pygame.KEYDOWN:
            
            match(event.key):
                case pygame.K_UP:
                    if game.snake.direction.y != 1:
                        game.snake.direction = Vector2(0, -1)
                case pygame.K_DOWN:
                    if game.snake.direction.y != -1:
                        game.snake.direction = Vector2(0, 1)
                case pygame.K_RIGHT:
                    if game.snake.direction.x != -1:
                        game.snake.direction = Vector2(1, 0)
                case pygame.K_LEFT:
                    if game.snake.direction.x != 1:
                        game.snake.direction = Vector2(-1, 0)



    screen.fill((175, 215, 70))
    game.draw_elements()
    pygame.display.update()
    clock.tick(60)