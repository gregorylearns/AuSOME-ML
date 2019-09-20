from Bio import SeqIO
from matplotlib import pyplot as plt
from collections import defaultdict
import numpy as np
from findpeaks import findpeaks
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import math
from scipy.optimize import curve_fit

a = 'DATA1'
b = 'DATA2'
c = 'DATA3'
d = 'DATA4'
e = 'DATA105'

channels = [a, b, c, d, e]
liz_500 = []
LIZ_500 = [500, 490, 450, 400, 350, 340, 300, 250, 200, 160, 150, 139, 100, 75, 50, 35]
Liz_500 = [35, 50, 75, 100, 139, 150, 160, 200, 250, 300, 340, 350, 400, 450, 490, 500]
for i in LIZ_500:
	liz_500.append(math.log(i))

record = SeqIO.read('A_GUI_12_2.fsa', 'abi')
trace = defaultdict(list)

for c in channels:
	trace[c] = record.annotations['abif_raw'][c]

# print(record.annotations.keys())

# plt.plot(trace[a], color='blue')
# plt.plot(trace[b], color='red')
# plt.plot(trace[c], color='green')
# plt.plot(trace[d], color='yellow')
# plt.plot(trace[e], color='black')

# plt.show()

# Normalize DATA105 (make all negative values zero)
data_105 = list(record.annotations['abif_raw'][e])
i = len(record.annotations['abif_raw'][e]) - 1

# for x in range(0, i):
# 	if data_105[x]<  0:
# 		data_105[x] = 0

indexes = findpeaks.findpeaks(data_105, spacing=50, limit=200)

ind = []
i = len(indexes) - 1
j = 0

while i >= 0:
	if j == 15:
		ind.append(indexes[i])
		break
	ind.append(indexes[i] + 1)
	j += 1
	i -= 1

print(ind)

x = np.array(ind).reshape((-1, 1))
y = np.array(LIZ_500)
x_ = PolynomialFeatures(degree=1, include_bias=False).fit_transform(x)
model = LinearRegression().fit(x_, y)

alelle = 3077

for c in range(0, len(ind)-1):
	if alelle > ind[c]:
		y_pred = ((alelle - ind[c])/((ind[c-1]-ind[c])/(LIZ_500[c-1]-LIZ_500[c]))+LIZ_500[c])
		break

print (y_pred)



# Logarithmic Regression
# def func(x, p1,p2):
#   return p1*np.log(x)+p2


# popt, pcov = curve_fit(func, x, y, p0=(1.0,10.2))

# # curve params
# p1 = popt[0]
# p2 = popt[1]

# y_pred = 3024*model.coef_ + model.intercept_ 
# y_pred = math.exp(y_pred)
# y_pred = 3024 * model.coef_ + model.intercept_ 
# print(y_pred)

# plt.plot(ind, LIZ_500, 'ro')
# plt.ylabel('Ladder fragments (in bp)')
# plt.show()

# 1
# 3024 - True(207 bp)
# 3482 - True(248 bp)
# 2037 - True(116 bp)
# 6219 - True(484 bp)
# 2
# 2068 - True(116 bp)
# 3077 - True(207 bp)
# 3096 - True(210 bp)
# 3629 - True(260 bp)