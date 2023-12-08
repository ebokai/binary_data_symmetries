from spin_tools import tools

d = [1, 2, 4, 6, 9, 11, 13, 14]
m = [3, 5, 9, 15]
q = [1, 14, 15]


print('data loops:')
ld = tools.loops(d)
print('model loops:')
lm = tools.loops(m)
print('comp loops:')
lq = tools.loops(q)

print(len(ld), len(lm), len(lq))

for l1 in ld:
	for l2 in ld:
		lx = set([x ^ y for x in l1 for y in l2])
		print(l1,l2,lx)