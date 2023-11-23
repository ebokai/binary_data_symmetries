import pygame
import numpy as np 
import draw
import states
import calc

XRES = 840
YRES = 600


pygame.init()
screen = pygame.display.set_mode((XRES, YRES))
bg_surface = pygame.Surface((XRES, YRES), pygame.SRCALPHA) 
bg_surface.fill((70, 70, 70))

distribution = [i for i in range(16)]
dk = calc.orthogonal_decomposition(distribution)
g = calc.model_couplings(distribution)
bg_surface = draw.draw_decomp(bg_surface, dk, distribution)
state_objects = states.init_states()

active = True
while active:

	bg_surface.fill((70, 70, 70))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			active = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			distribution = states.check_intersect(pos, state_objects)
			dk = calc.orthogonal_decomposition(distribution)
			g = calc.model_couplings(distribution)

	bg_surface = draw.draw_states(bg_surface, state_objects)
	bg_surface = draw.draw_decomp(bg_surface, dk, distribution)
	bg_surface = draw.draw_couplings(bg_surface, g)
	screen.blit(bg_surface, (0, 0))
	pygame.display.update()
