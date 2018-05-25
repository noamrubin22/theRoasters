import random

chance = []
pool = 10
prob = pool

for i in range(pool):
    for j in range(prob):
        chance.append(i)
    prob -= 1

keys = list(range(0, 10))
nlist = dict.fromkeys(keys)

for k in range(len(nlist)):
    nlist[k] = 0

# print(nlist)

for l in range(100000):
    num = chance[random.randint(0, len(chance) - 1)]
    nlist[num] += 1

print(nlist)
