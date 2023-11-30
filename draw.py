import pygame
import numpy as np

def draw_states(surface, states, block_size = 64):

	for state in states:
		state.pattern()
		surface.blit(state.surface, (state.x, state.y))

	return surface

def draw_decomp(surface, dk, distribution):

	X = 346

	font = pygame.font.SysFont('unispacebold', 16)

	for i in range(4):

		y = 16 + 48 * i

		bar = pygame.Surface((256, 32))
		bar.fill((255, 255, 255))
		bit = pygame.Surface((256 * dk[i]/4, 32))
		bit.fill((255, 0, 0))
		surface.blit(bar, (400, y))
		surface.blit(bit, (400, y))

		dx = font.render(f'D{i+1}:', False, (255, 255, 255))

		di = dk[i]
		if di < 1e-3:
			di = 0
		df = font.render(f'{di:.3g} bit', False, (255, 255, 255))
		surface.blit(dx, (X, y))
		surface.blit(df, (672, y))

	dc = font.render(f'Cumulative: {sum(dk):.3g} bit', False, (255, 255, 255))
	surface.blit(dc, (X, y + 48))

	if len(distribution) == 16:
		dist_str = 'all'
	else:
		dist_str = ','.join([str(x) for x in distribution])

	dd = font.render(f'States: [{dist_str}]', False, (255, 255, 255))
	surface.blit(dd, (X, y + 96))

	return surface

def draw_couplings(surface, g):

	nonzero = []
	couplings = []
	model_int = []

	X = 16
	Y = 346

	font = pygame.font.SysFont('unispacebold', 18)

	ops = ['0','1','2','12','3','13','23','123','4','14','24','124','34','134','234','1234']

	for i in range(1, 16):
		if abs(g[i]) > 1e-4:
			nonzero.append(ops[i])
			couplings.append(g[i])
			model_int.append(i)

	if len(couplings) > 0:
		amin = np.amin(np.abs(couplings))
	else:
		amin = 1

	model_check = check_group(model_int)
	if 0 in model_check:
		model_check.remove(0)
	model_check = sorted(model_check)


	dist_str = ','.join([str(x) for x in nonzero])
	model_id = np.power(2,model_int).sum()
	dd = font.render(f'Model: [{dist_str}] | ID: {model_id:.0f}', False, (255, 255, 255))
	surface.blit(dd, (X, Y))

	dist_str = ','.join([str(ops[x]) for x in model_check])
	check_id = np.power(2,model_check).sum()
	dd = font.render(f'Image: [{dist_str}] | ID: {check_id:.0f}', False, (255, 255, 255))
	surface.blit(dd, (X, Y + 36))

	coup_str = ','.join([f'{x/amin:.2g}' for x in couplings])
	dg = font.render(f'Couplings: [{coup_str}]', False, (255, 255, 255))
	surface.blit(dg, (X, Y + 72))

	props = ''
	if model_id == check_id:
		props += 'This model is a group'



	dg = font.render(f'Model size: [{len(couplings)}] | {props}', False, (255, 255, 255))
	surface.blit(dg, (X, Y + 108))

	

	return surface


def check_group(model):

	model.append(0)

	ops = []
	for op1 in model:
		for op2 in model:
			op3 = op1 ^ op2
			if op3 not in ops:
				ops.append(op3)
	return ops

