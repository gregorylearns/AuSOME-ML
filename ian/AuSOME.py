# load .fsa file
# scale ladder
# find all peaks between 35 bp to 500 bp
# get features of each peak
# store each peak and its features in array
# go through each element in array, feeding the model the peak's features
# get the peaks with '1' as label

from Bio import SeqIO
from ladder_fit import convert_to_bp, convert_to_index, find_lower, find_upper
from findpeaks import findpeaks as fp
import numpy as np
import pickle

model_name = 'Hsc40_model_RandomForest.sav'
model = pickle.load(open(model_name, 'rb'))

a = 'DATA1'
b = 'DATA2'
c = 'DATA3'
d = 'DATA4'

dye = [500, 490, 450, 400, 350, 340, 300, 250, 200, 160, 150, 139, 100, 75, 50, 35]

file = input('File to analyze: ')
record = SeqIO.read(file + '.fsa', 'abi')
data = record.annotations['abif_raw'][a]

label = []
area_of_peaks = []
no_of_peaks = []
length = []
peaks = []
height = []

index_35 = find_lower(record.annotations['abif_raw']['DATA105'], dye)
index_500 = find_upper(record.annotations['abif_raw']['DATA105'], dye)

detected_peaks = fp.findpeaks(data, spacing=25, limit=25)

for i in range(len(detected_peaks)-1):
	lower_end_of_window = detected_peaks[i] - 80
	upper_end_of_window = detected_peaks[i] + 20
	if lower_end_of_window < index_35 or upper_end_of_window > index_500:
		continue

	peaks.append(detected_peaks[i])
	area_of_peaks.append(np.trapz(data[lower_end_of_window:upper_end_of_window]))
	no_of_peaks.append(len(fp.findpeaks(data[lower_end_of_window:upper_end_of_window], spacing=5,limit=15)))
	length.append(round(convert_to_bp(detected_peaks[i], record.annotations['abif_raw']['DATA105'], dye)))
	height.append(data[detected_peaks[i]])


for i in range(len(peaks)-1):
	label.append(model.predict([[area_of_peaks[i], no_of_peaks[i], length[i], height[i]]]))

# print(peaks)
# print(len(peaks))
# print(label)

for x in range(len(label)-1):
	if label[x] == 1:
		print(length[x])
# print(label)

# A_COR_12_1_Hos.fsa