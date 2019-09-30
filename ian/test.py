import pandas as pd

file = pd.read_csv('Channel1.csv')
new_values1 = []
new_values2 = []
j = 0
for i in range(len(file)):
	new_values1.append(j)
	new_values2.append(j)
	j += 1

file["Height_column1"] = pd.Series(new_values1)
file["Height_column2"] = pd.Series(new_values2)

file.to_csv('test.csv')