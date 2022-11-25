from dataclasses import Field

import pygame


class Table:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = [[0 for _ in range(width)] for _ in range(height)]
        self.start_pos = self.random_start_pos()
        self.end_pos = self.random_end_pos()
        self.actual_pos = self.start_pos
        self.visited = []
        
    def get_cell(self, pos):
        x, y = pos
        return self.cells[y][x]
    
    def set_cell(self, pos, value):
        x, y = pos
        self.cells[y][x] = value
        
    def get_neighbours(self, pos):
        x, y = pos
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < self.width and 0 <= y + j < self.height:
                    neighbours.append(self.cells[y + j][x + i])
        return neighbours
    
    def get_click(self, mouse_pos):
        x, y = mouse_pos
        return x // self.cell_size, y // self.cell_size
    
    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x] == 0:
                    pygame.draw.rect(screen, pygame.Color('black'), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, pygame.Color('green'), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                    

     # returns a x, y coordinate of a random cell where the bot starts
    def random_start_pos(self):
        import random
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        return x, y
                
    def random_end_pos(self):
        import random
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        return x, y
    
    def draw_path(self, screen, path):
        for pos in path:
            pygame.draw.rect(screen, pygame.Color('red'), (pos[0] * self.cell_size, pos[1] * self.cell_size, self.cell_size, self.cell_size))
            
    def go_left(self):
        x, y = self.actual_pos
        if x > 0:
            self.actual_pos = x - 1, y
            self.visited.append(self.actual_pos)
    
    def go_right(self):
        x, y = self.actual_pos
        if x < self.width - 1:
            self.actual_pos = x + 1, y
            self.visited.append(self.actual_pos)
            
    def go_up(self):
        x, y = self.actual_pos
        if y > 0:
            self.actual_pos = x, y - 1
            self.visited.append(self.actual_pos)
            
    def go_down(self):
        x, y = self.actual_pos
        if y < self.height - 1:
            self.actual_pos = x, y + 1
            self.visited.append(self.actual_pos)
            
    def draw_actual_pos(self, screen):
        x, y = self.actual_pos
        pygame.draw.rect(screen, pygame.Color('blue'), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        
    def draw_start_pos(self, screen):
        x, y = self.start_pos
        pygame.draw.rect(screen, pygame.Color('yellow'), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        
    def draw_end_pos(self, screen):
        x, y = self.end_pos
        pygame.draw.rect(screen, pygame.Color('green'), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        
    def draw_visited(self, screen):
        for pos in self.visited:
            pygame.draw.rect(screen, pygame.Color('blue'), (pos[0] * self.cell_size, pos[1] * self.cell_size, self.cell_size, self.cell_size))
        
    def random_step(self):
        import random
        x, y = self.actual_pos
        rand = random.randint(0, 3)
        if rand == 0:
            self.go_left()
        elif rand == 1:
            self.go_right()
        elif rand == 2:
            self.go_up()
        else:
            self.go_down()
    
    def train(self, screen):
        self.draw_start_pos(screen)
        self.draw_end_pos(screen)
        while self.actual_pos != self.end_pos:
            self.random_step()
            self.draw_visited(screen)
        return self.visited
            
        
                
    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x] = 0


if __name__ == '__main__':
    window = pygame.display.set_mode((640, 480))
    # create a table of 16x16 cells
    table = Table(16, 16, 32)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = table.get_click(event.pos)
                table.set_cell(cell, 1)
        window.fill(pygame.Color('white'))
        table.render(window)
        table.train(window)
        pygame.display.flip()
    
    