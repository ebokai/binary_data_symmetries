from numba import njit
import numpy as np
import warnings
warnings.simplefilter('ignore')

@njit()
def fwht(u):
	v = u.copy()
	h = 1 
	lv = len(v)
	while h < lv:
		for i in range(0, lv, h * 2):
			for j in range(i, i + h):
				x = v[j]
				y = v[j + h]
				v[j] = x + y 
				v[j + h] = x - y 
		h *= 2
	return v

def bit_count(x):
	return bin(x).count('1')

def z(f,g):
	zz = np.sum(np.exp(np.dot(f,g)))
	pz = np.exp(np.dot(f,g))/zz
	return zz, pz

def dkl_fast(g, model, pdata, n):

	if len(model) != len(g):
		raise ValueError('The number of operators in model should match the number of parameters in g.')

	gx = np.zeros(2**n)
	gx[model] = g 

	h = fwht(gx)
	u = np.exp(h)
	z = np.sum(u)
	p = u/z 

	l = np.log(pdata/p)
	s = np.sum(l)

	if np.isnan(s) or np.isinf(s):
		l[np.isnan(l)] = 0
		l[np.isinf(l)] = 0

	dkl = pdata @ l 
	dkl_grad = fwht(p - pdata)

	return dkl, dkl_grad[model]

def kl_safe(p1, p2, bits = True):

	if bits:
		logp1p2 = np.log2(p1/p2)
	else:
		logp1p2 = np.log(p1/p2)

	logp1p2[np.isnan(logp1p2)] = 0 
	logp1p2[np.isinf(logp1p2)] = 0

	d = p1 @ logp1p2

	return d 

def nkron(n):

	f = np.array([[1,1],[1,-1]])

	if n == 1:
		return f 
	else:
		return np.kron(f, nkron(n - 1))