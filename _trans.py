

models = [
[3,6,10,15],
[9,10,12,15],
[3,5,10,12],
[3,6,9,12],
[5,6,12,15],
[3,5,9,15],
[5,6,9,10]]


for model in models:
	for op in range(16):
		t_mod = sorted([x ^ op for x in model])
		
		if model == t_mod:
			print(model, op)