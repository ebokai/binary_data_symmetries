import pygame 

class State(object):

	def __init__(self, x, y, label):
		self.x = x 
		self.y = y 
		self.active = True
		self.label = label
		self.block_size = 64
		self.surface = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
		self.surface.fill((255, 255, 255))
		self.active_surface = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
		self.active_surface.fill((0, 0, 255, 50))

	def pattern(self):

		self.surface.fill((255, 255, 255))

		for k in range(4):

			xk = self.block_size/2 * (k % 2)
			yk = self.block_size/2 * (k // 2)

			if (self.label & 2**k) != 0:

				spin_box = pygame.Surface((self.block_size/2, self.block_size/2))
				spin_box.fill((40, 40, 40))
				self.surface.blit(spin_box, (xk, yk))

		if not self.active:
			self.surface.blit(self.active_surface, (0, 0))


def check_intersect(pos, states):

	x, y = pos

	distribution = []

	for state in states:

		c1 = x > state.x 
		c2 = x < state.x + state.block_size
		c3 = y > state.y
		c4 = y < state.y + state.block_size

		if c1 * c2 * c3 * c4 != 0:
			state.active = not state.active

		if state.active:
			distribution.append(state.label)

	return distribution



def init_states():

	block_size = 64
	states = []

	m = 0

	for i in range(4):
		for j in range(4):

			x = block_size/4 * (j + 1) + block_size * j
			y = block_size/4 * (i + 1) + block_size * i

			state = State(x, y, m)
			states.append(state)

			m += 1

	return states