import numpy as np
import pygame

class snake():
    def __init__(self,size:tuple,cellSize:int, surface):
        self.Length = 3
        self.xoffset = (surface.get_width() - size[0]*cellSize)/2
        self.yoffset = (surface.get_height() - size[1]*cellSize)/2
        self.x = size[0]/2
        self.y = size[1]/2
        self.direction = (0,0)
        self.lastmove = (0,0)
        self.cellSize = cellSize
        self.surface = surface
        self.create_snake()
        
    def create_snake(self):
        segments = []
        for i in range(self.Length):
            segments.append(snakeSegment(self.x,self.y,self.xoffset,self.yoffset,self.cellSize,self.surface))
        self.segments = segments

    def add_segment(self):
        self.segments.append(snakeSegment(self.segments[-1].x, self.segments[-1].y,self.xoffset,self.yoffset,self.cellSize,self.surface))
        self.Length += 1  

    def update_position(self):
        for i in range(self.Length-1,-1,-1):
            if i>0:
                self.segments[i].x = self.segments[i-1].x
                self.segments[i].y = self.segments[i-1].y
            else:
                self.segments[i].x += self.direction[0] 
                self.segments[i].y += self.direction[1] 
                self.lastmove = self.direction

    def draw_snake(self):
        for i in range(self.Length):
            self.segments[i].draw_segment(self.cellSize-1)





class snakeSegment():
    def __init__(self,x,y, xoffset, yoffset, cellSize, surface):
        self.x = x
        self.y = y
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.cellSize = cellSize
        self.surface = surface

    def draw_segment(self,SegmentSize):
        segmentSquare = pygame.Rect(self.x * self.cellSize + self.xoffset,self.y * self.cellSize + self.yoffset,SegmentSize,SegmentSize)
        pygame.draw.rect(self.surface, "grey", segmentSquare)


