import numpy as np
import matplotlib.pyplot as plt

output = np.loadtxt("output_test.txt")

hits = 0
for elem in output[:, 2]:
    if elem <= 0.05:
        hits+=1
print(hits, hits/len(output[:, 2]))

plt.hist(output[:,2], bins = 50)
plt.show()
