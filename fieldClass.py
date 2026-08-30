import numpy as np
import pygame
import datetime as dt
class playing_Field():
    def __init__(self,size:tuple, cell_size:int ,surface):
        self.size = size
        self.cellSize = cell_size
        self.surface = surface
        self.xoffset = (surface.get_width() - size[0]*self.cellSize)/2
        self.yoffset = (surface.get_height() - size[1]*self.cellSize)/2
        self.create_field()
        self.create_walls()

    def create_field(self):
        field = []

        # Create a 2D grid of cells
        for j in range(self.size[1]):
            row = []
            for i in range(self.size[0]):
                row.append(cell(self.xoffset + i * self.cellSize, self.yoffset + j *self.cellSize, self.cellSize, self.surface))
            field.append(row)
        self.cells = field

    def create_walls(self):
        for cell in self.cells[0]:
            cell.add_wall()
        for cell in self.cells[-1]:
            cell.add_wall()
        for row in self.cells:
            row[0].add_wall()
            row[-1].add_wall()

        # self.cells[10][14].add_wall()
        
        # self.cells[10][12].add_wall()
        # self.cells[10][13].add_wall()
        # self.cells[10][15].add_wall()
        # self.cells[11][15].add_wall()
        # self.cells[9][12].add_wall()

    def start_flood_fill(self, x, y):
        self.reset_flood_fill()
        start = dt.datetime.now()
        queue = [(x, y)]
        self.cells[y][x].floodFillValue = 0  # Starting cell has a flood fill value of 0

        while queue:
            cell = queue[0]
            x, y = cell
            current_cell = self.cells[y][x]
            neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            for nx, ny in neighbors:
                if 0 <= nx < self.size[0] and 0 <= ny < self.size[1]:
                    neighbor_cell = self.cells[ny][nx]
                    if neighbor_cell.hasWall == 0 and neighbor_cell.floodFillValue == np.inf:
                        neighbor_cell.floodFillValue = current_cell.floodFillValue + 1
                        queue.append((nx, ny))
                    elif neighbor_cell.hasWall == 0 and neighbor_cell.floodFillValue > current_cell.floodFillValue + 1:
                        neighbor_cell.floodFillValue = current_cell.floodFillValue + 1
                        queue.append((nx, ny))
            queue.pop(0)

        end = dt.datetime.now()
        # print(f"Flood fill completed in: {str(dt.timedelta(seconds=(end - start).total_seconds()))} ")
            
                    
            
        
        
    def reset_flood_fill(self):
        for row in self.cells:
            for cell in row:
                cell.floodFillValue = np.inf

    def draw_field(self):
        for list in self.cells:
            for cell in list:
                cell.draw_cell()


class cell():
    def __init__(self,x,y, cell_size, surface):
        self.hasWall = 0
        self.hasApple = 0
        self.x = x
        self.y = y
        self.cellSize = cell_size
        self.surface = surface
        self.floodFillValue = np.inf  # Initialize with None

    def add_wall(self):
        self.hasWall = 1

    def add_apple(self):
        self.hasApple = 1

    def remove_apple(self):
        self.hasApple = 0
        
    def draw_cell(self):
        cellSquare = pygame.Rect(self.x, self.y, self.cellSize-1, self.cellSize-1)
       
        if self.hasWall == 1:
            colour = (20,20,60)
        elif self.hasApple == 1:
            colour = (255,0,0)
        else:
            colour = (25,80,25)

        pygame.draw.rect(self.surface, colour, cellSquare)

        # if pygame.font:
        #         font = pygame.font.Font(None, 11)
        #         text = font.render(str(self.floodFillValue), True, (255, 255, 255))
        #         text_rect = text.get_rect(center=cellSquare.center)
        #         self.surface.blit(text, text_rect)
