import numpy as np 
import calc
from itertools import combinations

np.set_printoptions(precision = 3, suppress = True)
n = 3
states = np.arange(2**n)

k1, k2, k3 = 0, 0, 0
n2s, n2m = 0, 0
kt = 0

models = []

for dist in combinations(states, 4):
	kt += 1
	dk = calc.orthogonal_decomposition(list(dist), n)
	g = calc.model_couplings(list(dist), n)

	model = []
	signs = []
	for i in range(1, 2**n):
		if abs(g[i]) > 1e-4:
			model.append(i)
			signs.append(np.sign(g[i]))

	dist_im = set([o1 ^ o2 for o1 in dist for o2 in dist])
	missing = [i for i in range(2**n) if i not in dist_im]

	print(dist, dk,  model, dist_im, missing)



	c0 = abs(dk[0]-1)
	c1 = abs(dk[1]-1)
	c2 = abs(dk[2]-1)


	if c0 < 1e-3:
		k1 += 1
		print('order 1:', dist, dk, model, dist_im, missing)
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
		print('order 2:', dist, dk, model, signs, model_id, dist_im, missing)
	elif c2 < 1e-3:
		k3 += 1
		print('order 3:', dist, dk, model, dist_im, missing)



print(f'k1: {k1}, k2: {k2} ({n2s}/{n2m}), k3: {k3} | kt: {kt}')
print(models)