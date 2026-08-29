import numpy as np
import pygame

class snake():
    def __init__(self,size:tuple,cellSize:int, surface):
        self.Length = 3
        self.xoffset = (surface.get_width() - size[0]*cellSize)/2
        self.yoffset = (surface.get_height() - size[1]*cellSize)/2
        self.x = int(size[0]/2)
        self.y = int(size[1]/2)
        self.direction = (0,-1)
        self.lastmove = (0,0)
        self.cellSize = cellSize
        self.surface = surface
        segments = []
        for i in range(self.Length):
            segments.append(snakeSegment(self.x,self.y,self.xoffset,self.yoffset,self.cellSize,self.surface))
        self.segments = segments

    def add_segment(self):
        self.segments.append(snakeSegment(self.segments[-1].x, self.segments[-1].y,self.xoffset,self.yoffset,self.cellSize,self.surface))
        self.Length += 1  

    def update_position(self,field):
        for i in range(self.Length-1,-1,-1):
            if i>0:
                self.segments[i].x = self.segments[i-1].x
                self.segments[i].y = self.segments[i-1].y
            else:
                self.segments[i].x += self.direction[0] 
                self.segments[i].y += self.direction[1] 
                self.lastmove = self.direction
        if self.wall_check(self.segments[0].x, self.segments[0].y, field):
            return False, True
        if self.apple_check(self.segments[0].x, self.segments[0].y, field):
            field.cells[self.segments[0].y][self.segments[0].x].remove_apple()
            self.add_segment()
            return True, False
        if self.snake_collision_check(self.segments[0].x, self.segments[0].y):
            return False, True
        return True, True

    def floodfillCheck(self,field):
        floodfill_values = []
        forwardcell = self.segments[0].x + 1*self.direction[0], self.segments[0].y + 1*self.direction[1]
        leftcell = self.segments[0].x + 1*(self.direction[0] + self.direction[1]), self.segments[0].y + 1*(self.direction[1] - self.direction[0])
        rightcell = self.segments[0].x + 1*(self.direction[0] - self.direction[1]), self.segments[0].y + 1*(self.direction[1] + self.direction[0])
        floodfill_values.append(field.cells[forwardcell[1]][forwardcell[0]].floodFillValue)
        floodfill_values.append(field.cells[leftcell[1]][leftcell[0]].floodFillValue)
        floodfill_values.append(field.cells[rightcell[1]][rightcell[0]].floodFillValue)
        return floodfill_values
    
    def wall_check(self,x,y,field):        
        if field.cells[y][x].hasWall == 1:
            return True
        return False

    def apple_check(self,x,y,field):
        if field.cells[y][x].hasApple == 1:
            return True
        return False

    def snake_collision_check(self,evalx,evaly):
        for i in range(1,self.Length):
            if evalx == self.segments[i].x and evaly == self.segments[i].y:
                return True
        return False

    def forward_check(self, field):
        collision = False
        headx = self.segments[0].x
        heady = self.segments[0].y
        
        
        if self.wall_check(headx + 1 * self.direction[0], heady + 1 * self.direction[1], field) or self.snake_collision_check(headx + 1 * self.direction[0], heady + 1 * self.direction[1]):
            collision = True
        else:
            collision = False

        return collision

    def right_check(self, field):
            collision = False
            headx = self.segments[0].x
            heady = self.segments[0].y
           
            if self.wall_check(headx + 1 * (self.direction[0] - self.direction[1]), heady + 1 * (self.direction[1] + self.direction[0]), field) or self.snake_collision_check(headx + 1 * (self.direction[0] - self.direction[1]), heady + 1 * (self.direction[1] + self.direction[0])):
                collision = True
            else:
                collision = False

            return collision

    def left_check(self, field):
            collision = False
            headx = self.segments[0].x
            heady = self.segments[0].y
           
           
            if self.wall_check(headx + 1 * (self.direction[0] + self.direction[1]), heady + 1 * (self.direction[1] - self.direction[0]), field) or self.snake_collision_check(headx + 1 * (self.direction[0] + self.direction[1]), heady + 1 * (self.direction[1] - self.direction[0])):
                collision = True
            else:
                collision = False

            return collision
    
    def draw_snake(self):
        for i in range(self.Length):
            self.segments[i].draw_segment(self.cellSize-1, i)




class snakeSegment():
    def __init__(self,x,y, xoffset, yoffset, cellSize, surface):
        self.x = x
        self.y = y
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.cellSize = cellSize
        self.surface = surface

    def draw_segment(self,SegmentSize, pos):
        segmentSquare = pygame.Rect(self.x * self.cellSize + self.xoffset,self.y * self.cellSize + self.yoffset,SegmentSize,SegmentSize)
        if pos == 0:
            pygame.draw.rect(self.surface, (30,30,30), segmentSquare)
        else:
            pygame.draw.rect(self.surface, (100,100,100), segmentSquare)


