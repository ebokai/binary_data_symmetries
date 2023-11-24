import tools
import numpy as np 
from scipy.optimize import minimize


def model_couplings(distribution):
	fn = tools.nkron(4)
	fi = np.linalg.inv(fn)

	p = np.ones(16)
	p[np.array(distribution)] = 1e10
	p = p / np.sum(p)

	g = fi @ np.log(p)

	return g

def orthogonal_decomposition(distribution):

	n = 4 

	# uniform distribution
	p0 = np.ones(2**n)/2**n

	# calculate empirical distribution
	p = np.zeros(2**n)
	u, c = np.unique(distribution, return_counts = True)
	p[u] = c / np.sum(c)
	pk = p 

	# spin matrix
	fn = tools.nkron(4)

	# distance from uniform distribution
	d0 = tools.kl_safe(p, p0)
	ds = 0
	# print(f'distance from uniform distribution: {d0:.3g} bits')

	dks = np.zeros(n)

	for i in range(n):

		order = n-1-i

		model = [op for op in np.arange(2**n) if tools.bit_count(op) <= order]

		min_result = minimize(tools.dkl_fast, np.zeros(len(model)), args = (model, pk, n), jac = True)

		zi, pi = tools.z(fn[:,model], min_result.x)

		dk = tools.kl_safe(pk, pi)
		
		ds += dk
		pk = pi 

		dks[order] = dk

		# print(f'information of order {order+1}: {dk:.3g} bits')

	# print(f'cumulative distance from uniform distribution: {ds:.3g} bits')

	return dks


