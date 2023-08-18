import pygame
import sys
import random

# Set up display
pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Tetris')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Define the Tetromino shapes
tetromino_shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]
tetromino_colors = [CYAN, YELLOW, RED, GREEN, BLUE, ORANGE, MAGENTA]

# Initialize game variables
score = 0
grid_size = (26, 20)
cell_size = (30, 30)
grid = [[0] * grid_size[0] for _ in range(grid_size[1])]


def draw_grid():
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            pygame.draw.rect(window, WHITE if grid[j][i] else BLACK,
                             (i * cell_size[0], j * cell_size[1], cell_size[0], cell_size[1]), 1)


def draw_tetromino(tetromino, pos, color):
    for i in range(len(tetromino)):
        for j in range(len(tetromino[i])):
            if tetromino[i][j]:
                pygame.draw.rect(window, color,
                                 (pos[0] * cell_size[0] + j * cell_size[0], pos[1] * cell_size[1] + i * cell_size[1],
                                  cell_size[0], cell_size[1]))
                pygame.draw.rect(window, BLACK,
                                 (pos[0] * cell_size[0] + j * cell_size[0], pos[1] * cell_size[1] + i * cell_size[1],
                                  cell_size[0], cell_size[1]), 1)


def check_collision(tetromino, pos):
    for i in range(len(tetromino)):
        for j in range(len(tetromino[i])):
            if tetromino[i][j]:
                if i + pos[1] >= grid_size[1] or j + pos[0] >= grid_size[0] or j + pos[0] < 0:
                    return True
                if grid[i + pos[1]][j + pos[0]]:
                    return True
    return False


def merge_tetromino(tetromino, pos, color_id):
    for i in range(len(tetromino)):
        for j in range(len(tetromino[i])):
            if tetromino[i][j]:
                grid[i + pos[1]][j + pos[0]] = color_id


def remove_lines():
    global score
    full_lines = [i for i, line in enumerate(grid) if all(line)]
    if full_lines:
        for i in full_lines:
            del grid[i]
            grid.insert(0, [0] * grid_size[0])
        score += len(full_lines)
    return len(full_lines)


def rotate_tetromino(tetromino):
    return [[tetromino[j][i] for j in range(len(tetromino))] for i in range(len(tetromino[0]) - 1, -1, -1)]


def main():
    global score
    clock = pygame.time.Clock()
    tetromino = random.choice(tetromino_shapes)
    color_id = random.randint(1, 7)
    pos = [grid_size[0] // 2 - len(tetromino[0]) // 2, 0]
    game_over = False
    while not game_over:
        window.fill(BLACK)
        draw_grid()
        draw_tetromino(tetromino, pos, tetromino_colors[color_id - 1])
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_pos = pos[:]
                    new_pos[0] -= 1
                    if not check_collision(tetromino, new_pos):
                        pos = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = pos[:]
                    new_pos[0] += 1
                    if not check_collision(tetromino, new_pos):
                        pos = new_pos
                elif event.key == pygame.K_DOWN:
                    new_pos = pos[:]
                    new_pos[1] += 1
                    if not check_collision(tetromino, new_pos):
                        pos = new_pos
                elif event.key == pygame.K_UP:
                    new_tetromino = rotate_tetromino(tetromino)
                    if not check_collision(new_tetromino, pos):
                        tetromino = new_tetromino

        pos[1] += 1
        if check_collision(tetromino, pos):
            pos[1] -= 1
            merge_tetromino(tetromino, pos, color_id)
            remove_lines()
            tetromino = random.choice(tetromino_shapes)
            color_id = random.randint(1, 7)
            pos = [grid_size[0] // 2 - len(tetromino[0]) // 2, 0]
            if check_collision(tetromino, pos):
                game_over = True

        clock.tick(5)

    print("Game Over! Your score:", score)


if __name__ == '__main__':
    main()
