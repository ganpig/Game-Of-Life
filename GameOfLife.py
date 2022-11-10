import sys
import time

import pygame

default = '''WINDOW_SIZE = (1000, 600)
BLOCK_SIZE = 20
BLOCK_SHAPE = 'square' # 'square' or 'circle'
SHOW_BORDER = True
BG_COLOR = (0, 0, 0)
FG_COLOR = (255, 255, 255)'''

try:
    exec(open('config.txt').read())
except:
    with open('config.txt', 'w', encoding='utf-8') as f:
        print(default, file=f)
        exec(default)
speed = 1
playing = False


def create_chart():
    ret = []
    for i in range(WINDOW_SIZE[0]//BLOCK_SIZE):
        ret.append(WINDOW_SIZE[1]//BLOCK_SIZE*[0])
    return ret


chart = create_chart()


def get(x, y):
    try:
        return chart[x][y]
    except:
        return 0


pygame.init()
pygame.key.set_repeat(500, 100)
screen = pygame.display.set_mode(WINDOW_SIZE)

start = time.time()
while True:
    screen.fill(BG_COLOR)
    for i, l in enumerate(chart):
        x = i*BLOCK_SIZE
        for j, a in enumerate(l):
            y = j*BLOCK_SIZE
            if SHOW_BORDER:
                if BLOCK_SHAPE == 'square':
                    pygame.draw.rect(screen, FG_COLOR, (x+1, y+1,
                                                        BLOCK_SIZE-2, BLOCK_SIZE-2), a ^ 1)
                elif BLOCK_SHAPE == 'circle':
                    pygame.draw.circle(
                        screen, FG_COLOR, (x+BLOCK_SIZE//2, y+BLOCK_SIZE//2), BLOCK_SIZE//2-1, a ^ 1)
            elif a:
                if BLOCK_SHAPE == 'square':
                    pygame.draw.rect(screen, FG_COLOR,
                                     (x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif BLOCK_SHAPE == 'circle':
                    pygame.draw.circle(
                        screen, FG_COLOR, (x+BLOCK_SIZE//2, y+BLOCK_SIZE//2), BLOCK_SIZE//2)
    pygame.display.flip()
    pygame.display.set_caption(
        f'Game of Life | Speed={speed} | UP/DOWN:change speed; Space:'+('play', 'pause')[playing]+'; Delete:clear')
    if playing and time.time()-start > 1/speed:
        new_chart = create_chart()
        for i in range(len(chart)):
            for j in range(len(chart[i])):
                tmp = get(i-1, j-1)+get(i-1, j)+get(i-1, j+1)+get(i, j-1) + \
                    get(i, j+1)+get(i+1, j-1)+get(i+1, j)+get(i+1, j+1)
                new_chart[i][j] = tmp == 3 or chart[i][j] and tmp == 2
        chart = new_chart
        start = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                speed += 0.25
            elif event.key == pygame.K_DOWN and speed > 0.25:
                speed -= 0.25
            elif event.key == pygame.K_SPACE:
                playing = not playing
            elif event.key == pygame.K_DELETE:
                chart = create_chart()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            chart[event.pos[0]//BLOCK_SIZE][event.pos[1]//BLOCK_SIZE] ^= 1
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            chart[event.pos[0]//BLOCK_SIZE][event.pos[1]//BLOCK_SIZE] = 1
