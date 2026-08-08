from Main import snakeGame
import pygame
game = snakeGame()
time_since_move = 0
action = 1
while game.running:
    time_since_move += game.clock.tick()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        action = 0
    elif keys[pygame.K_d]:
        action = 2
    if time_since_move > 500 and not keys[pygame.K_SPACE]:
        state, reward = game.step(action)
        print(state)
        print(reward)
        action = 1
        time_since_move = 0