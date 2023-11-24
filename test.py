import tools
import numpy as np 

print('------------------------------')
n = 4
model = [2, 12]
g = np.zeros((2**n))
g[model] = 17, -17

u = tools.fwht(g)
b = np.exp(u)
z = np.sum(b)
p = b / z 

for i in range(2**n):
	print(i, p[i])

fn = tools.nkron(n)
fi = np.linalg.inv(fn)

px = np.ones(16)
px[p > 1e-5] = 1e16
px = px / np.sum(px)
print(px)

gi = fi @ np.log(px)
print(np.where(np.abs(gi) > 1e-4))