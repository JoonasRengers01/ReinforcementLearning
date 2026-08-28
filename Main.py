import random
import numpy as np
import pygame
from snakeClass import snake
from fieldClass import playing_Field
class snakeGame():
    def __init__(self,locations):
        
        pygame.init()
        self.vertical_Cells = 20
        self.horizontal_Cells = 20
        self.cell_size = 20
        self.screen_Size = (1280,720)
        self.screen = pygame.display.set_mode(self.screen_Size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.snakeHead = snake((self.horizontal_Cells, self.vertical_Cells),self.cell_size,self.screen)
        self.play_area = playing_Field((self.horizontal_Cells,self.vertical_Cells),self.cell_size, self.screen)
        self.isApple = False
        self.appleX = None
        self.appleY = None
        self.max_distance =  0
        self.old_flood_fill = 10000
        self.locations = locations
    
        # random.seed(0)

    def observe(self):
        while not self.isApple:
                    self.appleX = self.locations[self.snakeHead.Length-3][0]
                    self.appleY = self.locations[self.snakeHead.Length-3][1]
                    if self.play_area.cells[self.appleY][self.appleX].hasWall == 0:
                        self.play_area.cells[self.appleY][self.appleX].add_apple()
                        # print(f"Apple placed at: {self.appleX}, {self.appleY}")
                        self.play_area.start_flood_fill(self.appleX,self.appleY)
                        floodfill_values = []
                        for row in self.play_area.cells:
                            for cell in row:
                                if cell.floodFillValue != 0 and cell.floodFillValue != 40:
                                    floodfill_values.append(cell.floodFillValue)
                        self.max_distance = max(floodfill_values)
                        self.old_flood_fill = self.play_area.cells[self.snakeHead.segments[0].y][self.snakeHead.segments[0].x].floodFillValue
                        self.isApple = True

        forward_apple_Distance = (self.appleX - self.snakeHead.segments[0].x) * self.snakeHead.direction[0] + (self.appleY - self.snakeHead.segments[0].y) * self.snakeHead.direction[1]
        sideways_apple_Distance = (self.appleY - self.snakeHead.segments[0].y) * self.snakeHead.direction[0] - (self.appleX - self.snakeHead.segments[0].x) * self.snakeHead.direction[1]
        self.screen.fill("black")
        self.play_area.draw_field()
        self.snakeHead.draw_snake()
        pygame.display.flip()
        return [float(self.play_area.cells[self.snakeHead.segments[0].y][self.snakeHead.segments[0].x].floodFillValue), float(forward_apple_Distance), float(sideways_apple_Distance),float(self.snakeHead.forward_check(self.play_area)), float(self.snakeHead.right_check(self.play_area)), float(self.snakeHead.left_check(self.play_area))]

    def step(self,action):

        while not self.isApple:
            self.appleX = random.randrange(2,self.horizontal_Cells-3)
            self.appleY = random.randrange(2,self.vertical_Cells-3)
            if self.play_area.cells[self.appleY][self.appleX].hasWall == 0:
                self.play_area.cells[self.appleY][self.appleX].add_apple()
                # print(f"Apple placed at: {self.appleX}, {self.appleY}")
                self.play_area.start_flood_fill(self.appleX,self.appleY)
                floodfill_values = []
                for row in self.play_area.cells:
                    for cell in row:
                        if cell.floodFillValue != 0 and cell.floodFillValue != 40:
                            floodfill_values.append(cell.floodFillValue)
                self.max_distance = max(floodfill_values)
                self.old_flood_fill = self.play_area.cells[self.snakeHead.segments[0].y][self.snakeHead.segments[0].x].floodFillValue
                self.isApple = True
                
                
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

       
        if action == 0:
            self.snakeHead.direction = (self.snakeHead.direction[1], -self.snakeHead.direction[0])
        elif action == 2:
            self.snakeHead.direction = (-self.snakeHead.direction[1], self.snakeHead.direction[0])
        
        
       
        
        if self.snakeHead.direction != (0,0):
            self.running,self.isApple = self.snakeHead.update_position(self.play_area)
            self.snakeHead.x += self.snakeHead.direction[0] * self.cell_size
            self.snakeHead.y += self.snakeHead.direction[1] * self.cell_size

        forward_apple_Distance = (self.appleX - self.snakeHead.segments[0].x) * self.snakeHead.direction[0] + (self.appleY - self.snakeHead.segments[0].y) * self.snakeHead.direction[1]
        sideways_apple_Distance = (self.appleY - self.snakeHead.segments[0].y) * self.snakeHead.direction[0] - (self.appleX - self.snakeHead.segments[0].x) * self.snakeHead.direction[1]
        if self.running:
            return_vector = [float(self.play_area.cells[self.snakeHead.segments[0].y][self.snakeHead.segments[0].x].floodFillValue), float(forward_apple_Distance), float(sideways_apple_Distance),float(self.snakeHead.forward_check(self.play_area)), float(self.snakeHead.right_check(self.play_area)), float(self.snakeHead.left_check(self.play_area))]
        else:
            return_vector = list(np.zeros(6))
        reward = 0
        if self.isApple:
            if self.play_area.cells[self.snakeHead.segments[0].y][self.snakeHead.segments[0].x].floodFillValue < self.old_flood_fill:
                reward += 50 - min(20,self.play_area.cells[self.snakeHead.segments[0].y][self.snakeHead.segments[0].x].floodFillValue)
            elif self.play_area.cells[self.snakeHead.segments[0].y][self.snakeHead.segments[0].x].floodFillValue > self.old_flood_fill:
                reward += -50 - min(20,(self.play_area.cells[self.snakeHead.segments[0].y][self.snakeHead.segments[0].x].floodFillValue))
            self.old_flood_fill = self.play_area.cells[self.snakeHead.segments[0].y][self.snakeHead.segments[0].x].floodFillValue
        else:
            reward = 400
            
        
        if not self.running:
            reward = -300

        self.screen.fill("black")
        self.play_area.draw_field()
        self.snakeHead.draw_snake()
        pygame.display.flip()
        return return_vector, reward, self.running
            

pygame.quit()


# Length, Snake X, Snake Y, Apple X, Apple Y, Forward free distance, Right free distance, Left free distance