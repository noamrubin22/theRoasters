from scores import scores
from scores1 import scores1
from scores2 import scores2
import numpy as np
import matplotlib.pyplot as plt


means = []
highs = []
lows = []

means3 = []
highs3 = []
lows3 = []

data = []
data3 = []
end = False

for i in range(len(scores2)):
    data3.append(scores2[i][1])

j = 0
for i in range(0, len(data3), 100):
    gen = []
    for j in range(100):
        j += i
        gen.append(data[j])
    data2.append(gen)

for i in range(len(data2)):
    means2.append(int(np.mean(data2[i])))
    highs2.append(int(np.amax(data2[i])))
    lows2.append(int(np.amin(data2[i])))
