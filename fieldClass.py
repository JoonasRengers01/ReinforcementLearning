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

        

    def start_flood_fill(self, x, y):
        self.reset_flood_fill()
        initialX = x
        initialY = y
        self.cells[initialY][initialX].floodFillValue = 1
        y -= 1
        self.recursive_flood_fill(x,y)
        count = 2
        while True:
            movedx = False
            movedy = False
            if y < initialY  and not movedx:
                if x - initialX == 0 and not movedy:
                    newy = y + 1
                    movedy = True
                newx = x + 1
                movedx = True
            elif y > initialY and not movedx:
                if x == initialX  and not movedy:
                    newy = y - 1
                    movedy = True
                newx = x - 1
                movedx = True
                

            if x > initialX and not movedy:
                if y == initialY and not movedx:
                    newx = x - 1
                    movedx = True
                newy = y + 1
                movedy = True
                
            elif x < initialX and not movedy:
                if y == initialY and not movedx:
                    newx = x + 1
                    movedx = True
                newy = y - 1
                movedy = True

            x = newx
            y = newy
            
            if x > self.size[0]-1 or x < 0 or y > self.size[1]-1 or y < 0:
                out_of_bounds = True

                while out_of_bounds:
                    if x > self.size[0]-1:
                        newx = self.size[0]-1
                        newy += 1
                    elif x < 0:
                        newx = 0
                        newy -= 1
                    elif y > self.size[1]-1:
                        newy = self.size[1]-1
                        newx -= 1
                    elif y < 0:
                        newy = 0   
                        newx += 1
                    
                    if 0 <= newx < self.size[0] and 0 <= newy < self.size[1]:
                        if self.cells[newy][newx].floodFillValue == 0:
                            x = newx
                            y = newy
                            out_of_bounds = False
                        else:
                            while self.cells[newy][newx].floodFillValue != 0:
                                
                                checkx = newx
                                checky = newy
                                if checkx == self.size[0]-1 and checky != self.size[1]-1:
                                    newy += 1
                                elif checkx == 0 and checky != 0:
                                    newy -= 1
                                if checky == self.size[1]-1 and checkx != 0:
                                    newx -= 1
                                elif checky == 0 and checkx != self.size[0]-1:
                                    newx += 1
                            x = newx
                            y = newy
                                
                    else:
                        if not (0 <= newx < self.size[0]):
                            x = newx
                        if not (0 <= newy < self.size[1]):
                            y = newy

            if self.cells[y][x].floodFillValue != 0:
                y -= 1
                movedy = True
                if y < 0:
                    y += 1
                    x += 1

                if x > self.size[0]-1:
                    x -= 1
                    y += 1


            

            

            if not movedx or not movedy:
                print("Error in flood fill movement logic")
            count += 1
            if count > self.size[0]*self.size[1]-1:
                break
            self.recursive_flood_fill(x,y)
            
            # self.cells[y][x].floodFillValue = count
            

        

    def recursive_flood_fill(self, x, y):
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        neighbor_values = []
        
        # print(f"Flood fill at ({x}, {y}), current value: {self.cells[y][x].floodFillValue}")
        for nx, ny in neighbors:
            if 0 <= nx < self.size[0] and 0 <= ny < self.size[1]:
                neighbor_cell = self.cells[ny][nx]
                if neighbor_cell.hasWall == 0 and neighbor_cell.floodFillValue != 0:
                    neighbor_values.append(neighbor_cell.floodFillValue)
        if self.cells[y][x].hasApple == 1:
            self.cells[y][x].floodFillValue = 1
        elif len(neighbor_values) > 0:
            self.cells[y][x].floodFillValue = min(neighbor_values) + 1
        else:
            self.cells[y][x].floodFillValue = 40
        if self.cells[y][x].hasWall == 1:
            self.cells[y][x].floodFillValue = 40
        
                    
    def flood_fill_check(self,x,y):
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        if self.cells[y][x].hasWall == 0:
            bigCount = 0
            neighbor_values = []
            for nx, ny in neighbors:
                if 0 <= nx < self.size[0] and 0 <= ny < self.size[1]:
                    neighbor_cell = self.cells[ny][nx]
                    # print(f"Checking neighbor at ({nx}, {ny}) with flood fill value: {neighbor_cell.floodFillValue}")
                    if neighbor_cell.hasWall == 0 and neighbor_cell.floodFillValue < self.cells[y][x].floodFillValue:
                        bigCount += 1
                        neighbor_values.append(neighbor_cell.floodFillValue)
            if bigCount > 2:
                print(f"Flood fill check at ({x}, {y}): {bigCount} neighbors with smaller flood fill value: {neighbor_values}, own flood fill value: {self.cells[y][x].floodFillValue}")   
                return False
        return True
            
        
        
    def reset_flood_fill(self):
        for row in self.cells:
            for cell in row:
                cell.floodFillValue = 0
            

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
        self.floodFillValue = 0  # Initialize with None

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
