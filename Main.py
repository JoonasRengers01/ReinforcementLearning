import random
import numpy as np
import pygame
from snakeClass import snake
from fieldClass import playing_Field
class snakeGame():
    def __init__(self):
        
        pygame.init()
        self.vertical_Cells = 20
        self.horizontal_Cells = 20
        self.cell_size = 30
        self.screen_Size = (1280,720)
        self.screen = pygame.display.set_mode(self.screen_Size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.snakeHead = snake((self.horizontal_Cells, self.vertical_Cells),self.cell_size,self.screen)
        self.play_area = playing_Field((self.horizontal_Cells,self.vertical_Cells),self.cell_size, self.screen)
        self.isApple = False
        self.appleX = None
        self.appleY = None


    def step(self,action):

        while not self.isApple:
            self.appleX = random.randrange(1,self.horizontal_Cells-2)
            self.appleY = random.randrange(1,self.vertical_Cells-2)
            if self.play_area.cells[self.appleY][self.appleX].hasWall == 0:
                self.play_area.cells[self.appleY][self.appleX].add_apple()
                self.isApple = True
                
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

       
        if action == 0:
            self.snakeHead.direction = (self.snakeHead.direction[1], -self.snakeHead.direction[0])
        elif action == 2:
            self.snakeHead.direction = (-self.snakeHead.direction[1], self.snakeHead.direction[0])
        
        self.screen.fill("black")
        self.play_area.draw_field()
        self.snakeHead.draw_snake()
        pygame.display.flip()
       
        
        if self.snakeHead.direction != (0,0):
            self.running,self.isApple = self.snakeHead.update_position(self.play_area)
            self.snakeHead.x += self.snakeHead.direction[0] * self.cell_size
            self.snakeHead.y += self.snakeHead.direction[1] * self.cell_size
        if self.running:
            return_vector = (self.snakeHead.Length, self.snakeHead.segments[0].x, self.snakeHead.segments[0].y, self.appleX, self.appleY, self.snakeHead.forward_check(self.play_area), self.snakeHead.right_check(self.play_area), self.snakeHead.left_check(self.play_area))
        else:
            return_vector = np.zeros(8)

        reward = self.snakeHead.Length - (1 - self.running) * 10
        return return_vector, reward
            

pygame.quit()


# Length, Snake X, Snake Y, Apple X, Apple Y, Forward free distance, Right free distance, Left free distance