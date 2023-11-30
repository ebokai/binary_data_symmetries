import numpy as np 
import calc
from itertools import combinations

np.set_printoptions(precision = 3, suppress = True)
n = 4
states = np.arange(2**n)

k1, k2, k3, k4 = 0, 0, 0, 0 
n2s, n2m = 0, 0
kt = 0

models = []

for dist in combinations(states, 8):
	kt += 1
	dk = calc.orthogonal_decomposition(list(dist))
	g = calc.model_couplings(list(dist))

	model = []
	signs = []
	for i in range(1, 16):
		if abs(g[i]) > 1e-4:
			model.append(i)
			signs.append(np.sign(g[i]))


	c0 = abs(dk[0]-1)
	c1 = abs(dk[1]-1)
	c2 = abs(dk[2]-1)
	c3 = abs(dk[3]-1)

	if c0 < 1e-3:
		k1 += 1
		print('order 1:', dist, dk, model)
	if c1 < 1e-3:
		k2 += 1
		if len(model) > 1:
			n2m += 1
			model_id = np.power(2,model).sum()
			if model_id not in models:
				models.append(model_id)
		else:
			n2s += 1
			model_id = 0
		print('order 2:', dist, dk, model, signs, model_id)
	elif c2 < 1e-3:
		k3 += 1
		print('order 3:', dist, dk, model)
	elif c3 < 1e-3:
		k4 += 1
		print('order 4:', dist, dk, model)

print(f'k1: {k1}, k2: {k2} ({n2s}/{n2m}), k3: {k3}, k4: {k4} | kt: {kt}')
print(models)