import pygame
import random

## GLOBAL VARS
screenHeight = 700
screenWidth = 700
playWidth = 300
playHeight = 600
cols = 10
rows = 20
block_size = 30

top_left_x = 100
top_left_y = (screenHeight - playHeight)

## SHAPE FORMATS
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 120, 0), (0, 0, 255), (180, 0, 180)]


class Tetrominos(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


class Tetris:
    def __init(self):
        pygame.init()

    ## RENDERING GUI
    def create_grid(self, locked_pos = {}):
        grid = [[(20, 20, 20) for _ in range(cols)] for _ in range(rows)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in locked_pos:
                    c = locked_pos[(j,i)]
                    grid[i][j] = c
        return grid


    def draw_grid(self, surface):
        sx = top_left_x
        sy = top_left_y

        for j in range(rows):
            pygame.draw.line(surface, (160, 160, 160), (sx, sy + j*block_size), (sx + playWidth, sy + j*block_size))
        for j in range(cols):
            pygame.draw.line(surface, (160, 160, 160), (sx + j*block_size, sy), (sx + j*block_size, sy + playHeight))


    def draw_window(self, surface, grid):
        surface.fill((10, 10, 10))

        pygame.font.init()
        font = pygame.font.SysFont("comicsans", 60)
        label = font.render("TETRIS", 1, (255, 255, 255))

        surface.blit(label, (top_left_x + playWidth//2 - (label.get_width()//2), 30))

        for i in range(rows):
            for j in range(cols):
                pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

        pygame.draw.rect(surface, (240, 160, 0), (top_left_x, top_left_y, playWidth, playHeight), 5)
        pygame.draw.line(surface, (255, 255, 255), (500, 0), (500, screenHeight), 3)
        self.draw_grid(surface)


    ##DRAW SIDEMENU
    def draw_next_tetromino(self, surface, tetromino, score=0):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", 24)
        label = font.render("Next Shape:", 1, (255, 255, 255))

        label_score = font.render("SCORE: " + str(score), 1, (255, 255, 255))

        format = tetromino.shape[tetromino.rotation % len(tetromino.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, tetromino.color, (520 + j*block_size, 300 + i*block_size, block_size, block_size))
        surface.blit(label, (520, 270))
        surface.blit(label_score, (520, 100))


    ## GAME LOGIC
    def get_shape(self):
        return Tetrominos(5, 0, random.choice(shapes))


    def render_tetrominos(self, tetromino):
        positions = []
        format = tetromino.shape[tetromino.rotation % len(tetromino.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((tetromino.x + j, tetromino.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
        return positions


    def collison_check(self, tetromino, grid):
        accepted_pos = [[(j, i) for j in range(cols) if grid[i][j] == (20, 20, 20)] for i in range(rows)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        positions = self.render_tetrominos(tetromino)
        for pos in positions:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True


    def check_lost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False


    def clear_rows(self, grid, locked_pos):
        inc = 0
        for i in range(len(grid)-1, -1, -1):
            row = grid[i]
            if (20, 20, 20) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked_pos[(j, i)]
                    except:
                        continue

        if inc > 0:
            for key in sorted(list(locked_pos), key = lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked_pos[newKey] = locked_pos.pop(key)

        return inc


    def run(self, surface):
        locked_pos = {}
        grid = self.create_grid(locked_pos)  ## play area
        change_piece = False
        run = True
        curr_tetromino = self.get_shape()
        next_tetromino = self.get_shape()
        score = 0

        clock = pygame.time.Clock()
        fspeed = 0.33
        ftime = 0
        # level = 0

        while run:
            grid = self.create_grid(locked_pos)
            ftime += clock.get_rawtime()
            # level += clock.get_rawtime()
            clock.tick()

            ## INCREASE FALL SPEED AS LEVEL INCREASES
            # if level / 1000 > 5:
            #     level_time = 0
            #     if fspeed > 0.12:
            #         fspeed -= 0.03


            if ftime / 1000 > fspeed:
                ftime = 0
                curr_tetromino.y += 1
                if not(self.collison_check(curr_tetromino, grid)) and curr_tetromino.y > 0:
                    curr_tetromino.y -= 1
                    change_piece = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        curr_tetromino.x -= 1
                        if not self.collison_check(curr_tetromino, grid):
                            curr_tetromino.x += 1

                    elif event.key == pygame.K_RIGHT:
                        curr_tetromino.x += 1
                        if not self.collison_check(curr_tetromino, grid):
                            curr_tetromino.x -= 1

                    elif event.key == pygame.K_DOWN:
                        # curr_tetromino.y += 1
                        fspeed = 0.08
                        if not self.collison_check(curr_tetromino, grid):
                            curr_tetromino.y -= 1

                    elif event.key == pygame.K_UP:
                        curr_tetromino.rotation += 1
                        if not self.collison_check(curr_tetromino, grid):
                            curr_tetromino.rotation -= 1

            tetromino_pos = self.render_tetrominos(curr_tetromino)
            # print(tetromino_pos)

            for i in range(len(tetromino_pos)):
                x, y = tetromino_pos[i]
                if y > -1:
                    # print(curr_tetromino.color)
                    grid[y][x] = curr_tetromino.color

            if change_piece:
                for pos in tetromino_pos:
                    p = (pos[0], pos[1])
                    locked_pos[p] = curr_tetromino.color

                fspeed = 0.30
                curr_tetromino = next_tetromino
                next_tetromino = self.get_shape()
                change_piece = False
                score += self.clear_rows(grid, locked_pos) * 10


            self.draw_window(surface, grid)
            self.draw_next_tetromino(surface, next_tetromino, score)
            pygame.display.update()

            if self.check_lost(locked_pos):
                run = False

        pygame.display.quit()




if __name__ == '__main__':
    win = pygame.display.set_mode((screenWidth, screenHeight))
    t = Tetris()
    t.run(win)
