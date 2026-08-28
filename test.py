from Main import snakeGame
import pygame
import numpy as np

time_since_move = 0
action = 1
np.random.seed(42)
randomlist = []
for i in range(50):
    randomlist.append((np.random.randint(2,17),np.random.randint(2,17)))
game = snakeGame(randomlist)
game.observe()
while game.running:
    time_since_move += game.clock.tick()

    
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_a]:
                action = 0
            elif keys[pygame.K_d]:
                action = 2
            state, reward, running = game.step(action)
            print(state)
            print(reward)
            action = 1
            time_since_move = 0