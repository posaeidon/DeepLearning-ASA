import numpy as np

output = np.loadtxt("output_ho.txt")

hits = 0
for elem in output[:, 2]:
    if elem <= 0.05:
        hits+=1
print(hits, hits/len(output[:, 2]))
