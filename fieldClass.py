import pygame

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

        self.cells[11][6].add_wall()
            

    def draw_field(self):
        for list in self.cells:
            for cell in list:
                cell.draw_cell()


class cell():
    def __init__(self,x,y, cell_size, surface):
        self.hasWall = 0
        self.x = x
        self.y = y
        self.cellSize = cell_size
        self.surface = surface

    def add_wall(self):
        self.hasWall = 1

        
    def draw_cell(self):
        cellSquare = pygame.Rect(self.x, self.y, self.cellSize-1, self.cellSize-1)
        
        if self.hasWall == 1:
            colour = (200,20,60)
        else:
            colour = (25,80,25)

        pygame.draw.rect(self.surface, colour, cellSquare)
