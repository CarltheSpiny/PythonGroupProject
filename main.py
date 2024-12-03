import pygame, sys, random
from pygame.math import Vector2

# GLOBAL VARIABLES
snake_color_options = ["blue", "green", "yellow", "purple", "orange", "pink"]
current_color_index = 0
snake_color = snake_color_options[current_color_index]


class Fruit:
    def __init__(self):
        self.randomize()
        self.color = pygame.Color("red")

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size
        )
        pygame.draw.rect(screen, self.color, fruit_rect)


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.color = pygame.Color(snake_color)
        self.direction = Vector2(-1, 0)
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
        global score
        global high_score
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            score += 1
            check_score(score)
            pygame.display.set_caption(
                "Snake. Score: " + str(score) + " High Score: " + str(high_score)
            )

    def check_fail(self):
        if (
            not 0 <= self.snake.body[0].x < cell_number
            or not 0 <= self.snake.body[0].y < cell_number
        ):
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        global score
        global high_score
        print("game over")
        menu("Game Over. Score:" + str(score), high_score, "RETRY")


class Button:
    def __init__(self, pos, text_input, font, base_color, hovering_color, size=(300, 100)):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width, self.height = size
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, "white")
        self.rect = pygame.Rect(
            self.x_pos - self.width // 2,
            self.y_pos - self.height // 2,
            self.width,
            self.height,
        )

    def update(self, screen):
        pygame.draw.rect(screen, self.base_color, self.rect, border_radius=5)
        screen.blit(self.text, self.text.get_rect(center=self.rect.center))

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.base_color = self.hovering_color
        else:
            self.base_color = "gray"


def get_font(size):
    return pygame.font.SysFont("bahnschrift", size)


def check_score(score_text):
    global high_score
    if score_text > high_score:
        high_score = score_text


def menu(title_text, high_score_text, button1):
    global screen
    global score
    global snake_color
    global current_color_index

    score = 0
    screen = pygame.display.set_mode((1280, 800))

    snake_color_button = Button(
        pos=(640, 700),
        text_input=snake_color.upper(),
        font=get_font(75),
        base_color="gray",
        hovering_color="red",
    )

    play_button = Button(
        pos=(640, 400), text_input=button1, font=get_font(75), base_color="gray", hovering_color="red"
    )
    quit_button = Button(
        pos=(640, 550), text_input="QUIT", font=get_font(75), base_color="gray", hovering_color="red"
    )

    while True:
        screen.fill("black")

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        title = get_font(100).render(title_text, True, "white")
        title_rect = title.get_rect(center=(640, 100))

        high_score_text_render = get_font(100).render(
            "High Score:" + str(high_score_text), True, "white"
        )
        high_score_rect = high_score_text_render.get_rect(center=(640, 250))

        screen.blit(title, title_rect)
        screen.blit(high_score_text_render, high_score_rect)

        for button in [play_button, quit_button, snake_color_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(MENU_MOUSE_POS):
                    game_loop()
                if quit_button.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if snake_color_button.checkForInput(MENU_MOUSE_POS):
                    # Cycle through the snake colors
                    current_color_index = (current_color_index + 1) % len(snake_color_options)
                    snake_color = snake_color_options[current_color_index]
                    snake_color_button.text_input = snake_color.upper()
                    snake_color_button.text = get_font(75).render(
                        snake_color_button.text_input, True, "white"
                    )

        pygame.display.update()


def game_loop():
    global score
    global high_score

    game = Game()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption(
        "Snake. Score: " + str(score) + " High Score: " + str(high_score)
    )
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SCREEN_UPDATE:
                game.update()

            if event.type == pygame.KEYDOWN:
                match event.key:
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


if __name__ == "__main__":
    pygame.init()
    cell_size = 40
    cell_number = 20
    screen_size = cell_number * cell_size

    score = 0
    high_score = 0
    pygame.display.set_caption("Snake")
    menu("Snake Game", high_score, "START")
