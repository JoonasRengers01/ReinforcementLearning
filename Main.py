import random

import pygame
from snakeClass import snake
from fieldClass import playing_Field

pygame.init()
vertical_Cells = 20
horizontal_Cells = 20
cell_size = 30


screen_Size = (1280,720)


screen = pygame.display.set_mode(screen_Size)
clock = pygame.time.Clock()
running = True
snakeHead = snake((horizontal_Cells, vertical_Cells),cell_size,screen)
play_area = playing_Field((horizontal_Cells,vertical_Cells),cell_size, screen)
time_since_move = 0
gameSpeed = 500
isApple = False


while running:

    while not isApple:
        appleX = random.randrange(1,horizontal_Cells-2)
        appleY = random.randrange(1,vertical_Cells-2)
        if play_area.cells[appleY][appleX].hasWall == 0:
            play_area.cells[appleY][appleX].add_apple()
            isApple = True
            if gameSpeed > 100:
                gameSpeed -= 10
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_s] and snakeHead.lastmove != (0,-1):
        snakeHead.direction = (0,1)
    if keys[pygame.K_w] and snakeHead.lastmove != (0,1):
        snakeHead.direction = (0,-1)
    if keys[pygame.K_a] and snakeHead.lastmove != (1,0) :
        snakeHead.direction = (-1,0)
    if keys[pygame.K_d] and snakeHead.lastmove != (-1,0):
        snakeHead.direction = (1,0)
    if keys[pygame.K_SPACE]:
        snakeHead.add_segment()

    
    
    screen.fill("black")
    play_area.draw_field()
    snakeHead.draw_snake()
    pygame.display.flip()
    dt = clock.tick(60)
    time_since_move += dt
    print(dt)
    
    if time_since_move >= gameSpeed:
        time_since_move = 0
        if snakeHead.direction != (0,0):
            running,isApple = snakeHead.update_position(play_area)
        snakeHead.x += snakeHead.direction[0] * cell_size
        snakeHead.y += snakeHead.direction[1] * cell_size
        

pygame.quit()