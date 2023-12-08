import numpy as np
from spin_tools import tools
import calc
import matplotlib.pyplot as plt 

p = [0, 4, 5, 7, 8, 10, 11, 15]
fig, axs = plt.subplots(4,4)
axs = axs.flatten()

for o in range(16):

	pt = [o ^ s for s in p]

	pd = np.zeros((4,4))

	for x in pt:
		i = x % 4  
		j = x // 4
		pd[i,j] = 1

	axs[o].set_title(o)
	axs[o].imshow(pd)
	axs[o].set_xticks([])
	axs[o].set_yticks([])

plt.show()


	