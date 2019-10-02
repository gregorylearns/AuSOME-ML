import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

file = pd.read_csv('Channel1_Data.csv')
# file = file.drop(['Unnamed: 0'], axis=1)

height = []

for i in range(len(file)):
	if file.iat[i, 0] != 'POP':
		if file.iat[i, 3] == file.iat[i, 4]:
			height.append(file.iat[i, 3])
		else:
			height.append(file.iat[i, 3])
			height.append(file.iat[i, 4])

h = np.histogram(height, bins='fd')
# plt.hist(height1, bins='fd')

# plt.hist(height2, bins='fd')
# plt.show()
new_values1 = []
new_values2 = []

for c in range(len(file)):
	if file.iat[c, 0] != 'POP':
		for i in range(len(h[1])):
			if file.iat[c, 3] <= h[1][i]:
				new_values1.append(round(h[1][i-1], 2))
				break
		for j in range(len(h[1])):
			if file.iat[c, 4] <= h[1][j]:
				new_values2.append(round(h[1][j-1], 2))
				break

print(len(new_values1))
print(len(new_values2))
# print(new_values1)
c = 0

for i in range(len(file)):
	if file.iat[i, 0] != 'POP':
		if c <= 412:
			file.iat[i, 3] = new_values1[c]
			file.iat[i, 4] = new_values2[c]
			c += 1

print(c)
# file["Height_column1"] = pd.Series(new_values1)
# file["Height_column2"] = pd.Series(new_values2)

file.to_csv('Channel1_Data_Normalized.csv', index=False)
