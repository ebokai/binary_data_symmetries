import numpy as np 
from spin_tools import tools
from scipy.optimize import minimize
import matplotlib.pyplot as plt 
from spin_tools import information_geometry as ig 

n = 7
fn = tools.nkron(n)

k = np.random.randint(1,2**n-1)
model = np.random.choice(np.arange(1,2**n), k, replace = False)
pars = np.random.uniform(-0.2,0.2,len(model))
g = np.zeros(2**n)
g[model] = pars
u = np.exp(fn @ g)
z = np.sum(u)
p = u / z  

data = np.random.choice(np.arange(2**n), 150, p = p)
N = len(data)
pk, dk = ig.orthogonal_decomposition(n, data)
print(dk)
u,c = np.unique(data, return_counts = True)
ndata = np.zeros(2**n)
pdata = np.zeros(2**n)
ndata[u] = c
pdata[u] = c / np.sum(c)

q_counts = []
q_states = []
for i in range(np.amax(c)+1):
    q = list(np.where(ndata==i)[0])
    if len(q) > 0:
        q_counts.append(i)
        q_states.append(q)
q_counts = np.array(q_counts)
log_q = np.log(q_counts/N, where = q_counts > 0)
print(q_counts)
print(q_states)
ri = np.log(q_counts)
print('ri:',ri)

# construct chi operators
fq = []
for states in q_states:
    ch = np.sum(fn[states,:], axis=0) # dividing by 2^n gives the SVD in the paper
    fq.append(ch)
fq = np.array(fq)
print(fq.shape)
print(fq)
print('log q:',log_q)

fq0 = fq.copy()
fq0[np.abs(fq0) <= 1] = 0
print(fq0)


plt.subplot(121)
plt.title('Full FQ')
w, s, u = np.linalg.svd(fq[:,1:], full_matrices = False) 
print('singular values:', s/2**n)
psi = np.dot(fn[:,1:], u.T)

# for i in range(psi.shape[1]):
# 	plt.plot(psi[:,i])

for l in range(2,psi.shape[1]+1):
    g0 = np.zeros(l)
    min_result = minimize(tools.dkl, x0=g0, args=(psi[:,:l], pdata), jac = True, tol = 1e-3)
    g = min_result.x
    print(g)
    u = np.exp(psi[:,:l] @ g)
    z = np.sum(u)
    p = u / z 
    plt.plot(p, pdata, '.',label=l)

    data = np.random.choice(np.arange(2**n), 1000, p = p)
    ig.orthogonal_decomposition(n, data)
plt.xlim(1e-3,0.1)
plt.ylim(1e-3,0.1)
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.subplot(122)
plt.title('Truncate small sums')
w, s, u = np.linalg.svd(fq0[:,1:], full_matrices = False) 
print('singular values:', s/2**n)
psi = np.dot(fn[:,1:], u.T)

# for i in range(psi.shape[1]):
# 	# plt.plot(psi[:,i])

for l in range(2,psi.shape[1]+1):
    g0 = np.zeros(l)
    min_result = minimize(tools.dkl, x0=g0, args=(psi[:,:l], pdata), jac = True, tol = 1e-3)
    g = min_result.x
    print(g)

    u = np.exp(psi[:,:l] @ g)
    z = np.sum(u)
    p = u / z 
    plt.plot(p, pdata, '.',label=l)
plt.xlim(1e-3,0.1)
plt.ylim(1e-3,0.1)
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.show()