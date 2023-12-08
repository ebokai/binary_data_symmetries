import numpy as np 
import calc
from spin_tools import tools
import matplotlib.pyplot as plt

np.set_printoptions(precision = 5, suppress = True)


n = 4 
fn = tools.nkron(n)
m = [3, 5, 10, 12]
sgn = [[-1,1,1,1],[1,-1,1,1],[1,1,-1,1],[1,1,1,-1],[1,-1,-1,-1],[-1,1,-1,-1],[-1,-1,1,-1],[-1,-1,-1,1]]

c = ['k','r','b','g']
g = np.zeros(2**n)
alpha = 10
i = 0

fig, axs = plt.subplots(2,4, figsize = (16, 9), sharex = True, sharey = True)
axs = axs.flatten()

for s in sgn:

	axs[i].set_aspect('equal')

	g[m] = np.array(s) * alpha
	u = np.exp(fn @ g)
	z = np.sum(u)
	p = u / z 

	ls = np.where(p > 0.01)[0]
	print(s, ls)

	for l in ls[:4]:
		print(l, 15-l)
		axs[i].plot([np.cos(2*np.pi*l/16),np.cos(2*np.pi*(15-l)/16)], [np.sin(2*np.pi*l/16),np.sin(2*np.pi*(15-l)/16)], c = c[i % 4])
		axs[i].plot([np.cos(2*np.pi*l/16),np.cos(2*np.pi*(15-l)/16)], [np.sin(2*np.pi*l/16),np.sin(2*np.pi*(15-l)/16)], 'o', c = c[i % 4])


	for l1 in ls:
		for l2 in ls:

			if l1 != l2:

				axs[i].plot([np.cos(2*np.pi*l1/16),np.cos(2*np.pi*(l2)/16)], [np.sin(2*np.pi*l1/16),np.sin(2*np.pi*(l2)/16)], c = c[i % 4], ls = '--', lw=1, alpha = 0.5)


	X = np.linspace(0,2*np.pi)
	axs[i].plot(np.cos(X), np.sin(X), ls = ':', c= 'k')
	axs[i].set_title(s)
	



	axs[i].set_xlim(-2,2)
	axs[i].set_ylim(-2,2)

	i += 1

# plt.show()

plt.savefig('coset_state_match.pdf',bbox_inches='tight')