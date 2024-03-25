import pygame
import random

height_win = 600
width_win = 1100
speed_game = 1000
game_width = 600
game_height = 600
block_size = 30

RED = (220, 10, 10)
GREEN = (15, 240, 10)
YEllOW = (220, 200, 10)
PURPLE = (220, 10, 220)
GREY = (244, 244, 244)
BLACK = (0, 0, 0)

pygame.mixer.init()
pygame.mixer.music.load('music/back.ogg')
pygame.mixer.music.play(-1)
pygame.mixer_music.set_volume(0.1)

def show_text(text, x, y):
    font = pygame.font.SysFont('Century Gothic', 30)
    text = font.render(text, True, (253, 255, 237))
    window.blit(text, (x, y))

class Board:
    def __init__(self):
        self.grid = []
        self.count_w = game_width//block_size
        self.count_h = game_height//block_size
        for i in range(self.count_h):
            tm = []
            for j in range(self.count_w):
                tm.append(0)
            self.grid.append(tm)

    def draw(self):
        for y in range(self.count_h):
            #print(self.grid[y])
            for x in range(self.count_w):
                if self.grid[y][x]:
                    pygame.draw.rect(window, RED, (block_size*x, block_size*y, block_size, block_size))
                    pygame.draw.rect(window, GREY, (block_size*x, block_size*y, block_size, block_size), 1)
                #else:
                    #ввpygame.draw.rect(window, GREY, (block_size * x, block_size * y, block_size, block_size), 1)

    def check_line(self):
        lines_to_delete = []
        for y in range(len(self.grid)):
            if all(self.grid[y]):
                lines_to_delete.append(y)
        for line in lines_to_delete:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(self.count_w)])

        for _ in range(len(lines_to_delete)):
            for y in range(len(self.grid) - 1, 0, -1):
                for x in range(len(self.grid[y])):
                    self.grid[y][x] = self.grid[y - 1][x]
            self.grid[0] = [0 for _ in range(self.count_w)]

    def clear_board(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                self.grid[y][x] = 0
class Figures:
    shapes = [
        [[1, 1, 1, 1]],

        [[1, 1, 1, 1],
         [1, 0, 0, 1]],

        [[1, 0, 0, 1],
         [1, 1, 1, 1]],

        [[1, 1],
         [1, 1]],

        [[1, 1, 1],
         [0, 1, 0]],

        [[0, 1, 0],
         [1, 1, 1]],

        [[1, 1, 1],
         [1, 0, 0]],

        [[1, 1, 1],
         [0, 0, 1]],

        [[1, 0],
         [1, 1],
         [0, 1]],

        [[1, 1],
         [0, 1],
         [0, 1]],

        [[0, 1],
         [1, 1],
         [0, 1]],

        [[1, 0],
         [1, 0],
         [1, 1]],

        [[1, 1],
         [1, 0],
         [1, 0]],
    ]
    def __init__(self):
        self.shape = random.choice(self.shapes)
        self.x = game_width // 2
        self.y = 0
        self.speed_y = 5
    def draw(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    pygame.draw.rect(window, GREEN, ((self.x) + x * block_size, (self.y) + y * block_size, block_size, block_size))

    def update(self, board):
        if self.can_move(0, self.speed_y, board):
            self.y += self.speed_y
        else:
            self.add_to_board(board)
            self.__init__()

    def can_move(self, dx, dy, board):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    new_x = self.x + dx + x * block_size
                    new_y = self.y + dy + y * block_size
                    board_y = self.y // block_size + y + 1
                    board_x = self.x // block_size + x
                    if (new_x < 0 or new_x > game_width - block_size or
                            new_y > game_height - block_size or
                            board_y >= len(board.grid) or board_x >= len(board.grid[0]) or
                            board.grid[board_y][board_x]):
                            return False
        return True


    def move_player(self, dx, board):
        if self.can_move(dx, 0, board):
            self.x += dx

    def add_to_board(self, board):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    board_y = self.y // block_size + y
                    board_x = self.x // block_size + x
                    board.grid[board_y][board_x] = 1

def restart_game():
    game_board.clear_board()

pygame.init()
window = pygame.display.set_mode((width_win, height_win))
clock = pygame.time.Clock()

game_board = Board()
shape = Figures()
while True:
    window.fill(BLACK)
    show_text("TETRIS", 800, 100)
    show_text("A - влево, D - вправо", 700, 150)
    show_text("R - рестарт", 760, 200)
    pygame.draw.rect(window, GREY, (0, 0, game_width, game_height), 2)
    shape.draw()
    game_board.draw()
    shape.update(game_board)
    game_board.check_line()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        exit()
    if keys[pygame.K_d]:
        shape.move_player(5, game_board)
    if keys[pygame.K_a]:
        shape.move_player(-5, game_board)
    if keys[pygame.K_r]:
        restart_game()

    clock.tick(60)
    pygame.display.update()