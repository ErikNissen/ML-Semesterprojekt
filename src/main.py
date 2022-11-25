import math

import pygame


class Table:
	def __init__(self, width, height, cell_size, screen):
		self.width = width
		self.height = height
		self.cell_size = cell_size
		self.cells = [[0 for _ in range(width)] for _ in range(height)]
		self.start_pos = self.random_start_pos()
		self.end_pos = self.random_end_pos()
		self.actual_pos = self.start_pos
		self.visited = []
		self.screen = screen
		self.steps = 0

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
				pygame.draw.rect(
						screen, pygame.Color('black'),
						(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size), 1
				)

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
			pygame.draw.rect(
					screen, pygame.Color('red'),
					(pos[0] * self.cell_size, pos[1] * self.cell_size, self.cell_size, self.cell_size)
			)

	def go_left(self):
		x, y = self.actual_pos
		if x > 0:
			self.actual_pos = x - 1, y
			self.visited.append([self.actual_pos, math.pow(0.91, self.steps)])

	def go_right(self):
		x, y = self.actual_pos
		if x < self.width - 1:
			self.actual_pos = x + 1, y
			self.visited.append([self.actual_pos, math.pow(0.91, self.steps)])

	def go_up(self):
		x, y = self.actual_pos
		if y > 0:
			self.actual_pos = x, y - 1
			self.visited.append([self.actual_pos, math.pow(0.91, self.steps)])

	def go_down(self):
		x, y = self.actual_pos
		if y < self.height - 1:
			self.actual_pos = x, y + 1
			self.visited.append([self.actual_pos, math.pow(0.91, self.steps)])

	def draw_actual_pos(self, screen):
		x, y = self.actual_pos
		pygame.draw.rect(
				screen, pygame.Color('blue'), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
		)

	def draw_start_pos(self, screen):
		x, y = self.start_pos
		pygame.draw.rect(
				screen, pygame.Color('yellow'), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
		)

	def draw_end_pos(self, screen):
		x, y = self.end_pos
		pygame.draw.rect(
				screen, pygame.Color('green'), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
		)

	def draw_visited(self):
		for cell in self.visited:
			pos = cell[0]
			points = cell[1]
			# format the points to #.###+e##
			points = f"{points:.2e}"
			# get actual color of the cell
			color = self.screen.get_at(
					(pos[0] * self.cell_size + self.cell_size // 2, pos[1] * self.cell_size + self.cell_size // 2)
					)
			if color == pygame.Color('blue'):
				pygame.draw.rect(
						self.screen, pygame.Color('white'),
						(pos[0] * self.cell_size, pos[1] * self.cell_size, self.cell_size, self.cell_size)
				)
			self.draw_text_in_cell(points, pos)
			x, y = pos

			r = pygame.Surface((self.cell_size, self.cell_size))
			r.set_alpha(1)
			r.fill(pygame.Color('red'))
			self.screen.blit(r, (x * self.cell_size, y * self.cell_size))

	def draw_text_in_cell(self, text, pos):
		# check if is text in the cell
		if self.screen.get_at((pos[0] * self.cell_size + self.cell_size // 2, pos[1] * self.cell_size + self.cell_size // 2)) != pygame.Color('white'):
			return 
		# draw the text in the cells in the middle
		pygame.font.init()
		font = pygame.font.SysFont('Arial', 18)
		text = font.render(f"{text}", True, pygame.Color('black'))
		text_rect = text.get_rect(
			center=(pos[0] * self.cell_size + self.cell_size // 2, pos[1] * self.cell_size + self.cell_size // 2)
			)
		self.screen.blit(text, text_rect)

	def is_visited(self, pos):
		# return False
		return pos in self.visited

	def random_step(self):
		import random
		x, y = self.actual_pos
		rand = random.randint(0, 3)
		if rand == 0:
			self.steps += 1
			self.go_left()
		elif rand == 1:
			self.steps += 1
			self.go_right()
		elif rand == 2:
			self.steps += 1
			self.go_up()
		elif rand == 3:
			self.steps += 1
			self.go_down()
		self.set_cell(self.actual_pos, 1)

	def draw_steps(self):
		# draws the number of steps in the bottom left corner
		pygame.font.init()
		font = pygame.font.SysFont('Arial', 20)
		text = font.render(f"Step: {self.steps}", True, pygame.Color('black'))
		text_rect = text.get_rect(
			center=(self.width * self.cell_size // 2, self.height * self.cell_size + self.cell_size // 2)
			)
		self.screen.blit(text, text_rect)

	def update(self):
		self.clear()
		self.render(self.screen)
		self.set_cell(self.start_pos, 1)
		self.set_cell(self.end_pos, 1)
		self.draw_text_in_cell('S', self.start_pos)
		self.draw_text_in_cell('E', self.end_pos)
		self.draw_start_pos(self.screen)
		self.draw_end_pos(self.screen)
		self.draw_visited()
		self.draw_steps()
		self.draw_actual_pos(self.screen)
		pygame.display.flip()
		pygame.time.wait(1000 // 60)

	def train(self):
		while self.actual_pos != self.end_pos:
			self.random_step()
			self.update()

	def clear(self):
		self.screen.fill(pygame.Color('white'))


if __name__ == '__main__':
	window = pygame.display.set_mode((1080, 1080))
	# create a table of 16x16 cells
	table = Table(16, 16, 64, window)
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				cell = table.get_click(event.pos)
				table.set_cell(cell, 1)
		window.fill(pygame.Color('white'))
		table.train()
