from Bio import SeqIO
from matplotlib import pyplot as plt
from collections import defaultdict
import numpy as np
import math
from ladder_fit import convert_to_bp, convert_to_index, find_lower, find_upper

a = 'DATA1'
b = 'DATA2'
c = 'DATA3'
d = 'DATA4'
e = 'DATA105'

channels = [a, b, c, d, e]
dye = [500, 490, 450, 400, 350, 340, 300, 250, 200, 160, 150, 139, 100, 75, 50, 35]

record = SeqIO.read('A_COR_12_1_Hos.fsa', 'abi')
trace = defaultdict(list)

for c in channels:
	trace[c] = record.annotations['abif_raw'][c]

# plt.plot(trace[a], color='blue')
# plt.plot(trace[b], color='red')
# plt.plot(trace[c], color='green')
# plt.plot(trace[d], color='yellow')
# plt.plot(trace[e], color='black')

# plt.show()
# converted_bp = convert_to_bp(1370, record.annotations['abif_raw'][e], dye)
# print(converted_bp)

# converted_index = convert_to_index(240.27, record.annotations['abif_raw'][e])
# print(converted_index)
alelle = 288
height = []
index_of_peaks = []
data1 = list(record.annotations['abif_raw'][a])

for c in range(find_lower(record.annotations['abif_raw'][e], dye), find_upper(record.annotations['abif_raw'][e], dye)):
	converted_bp = convert_to_bp(c, record.annotations['abif_raw'][e], dye)
	in_range = converted_bp >= alelle - 1 and converted_bp <= alelle + 1
	if in_range:
		index_of_peaks.append(c)
		height.append(data1[c])
	elif converted_bp > alelle:
		break

print(height)
print(index_of_peaks)
print(max(height))
print(convert_to_bp(1175, record.annotations['abif_raw'][e], dye))

# Make negative values in array zero
# data_105 = list(record.annotations['abif_raw'][e])
# i = len(record.annotations['abif_raw'][e])

# for x in range(0, i):
# 	if data_105[x] <  0:
# 		data_105[x] = 0

# indexes = findpeaks.findpeaks(data_105, spacing=50, limit=200)

# ind = []
# i = len(indexes) - 1
# j = 0

# while i >= 0:
# 	ind.append(indexes[i])
# 	j += 1
# 	i -= 1

# alelle = 3453

# for c in range (0, len(ind)-1):
# 	if alelle > ind[c]:
# 		y_pred = ((alelle - ind[c])/((ind[c-1]-ind[c])/(LIZ_500[c-1]-LIZ_500[c]))) + LIZ_500[c]
# 		break

# print (y_pred)

# 1
# 3024 - True(207 bp)
# 3482 - True(248 bp)
# 2037 - True(116 bp)
# 6219 - True(484 bp)

# 2
# 2068 - True(116 bp)
# 3077 - True(210 bp)
# 3096 - True(212 bp)
# 3629 - True(260 bp)

# 4
# 2996 - True(199 bp)
# 3042 - True(203 bp)
# 3256 - True(222 bp)
# 3453 - True(240 bp)
# 3736 - True(264 bp)
# 6330 - True(484? bp)

# 5
# 