from Bio import SeqIO
from matplotlib import pyplot as plt
from collections import defaultdict
import numpy as np
import pandas as pd
import math
from ladder_fit import convert_to_bp, convert_to_index, find_lower, find_upper
from tqdm import tqdm

my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
file = pd.read_csv(my_dir+'HSC24-A_Channel2.csv')
a = 'DATA1'
b = 'DATA2'
c = 'DATA3'
d = 'DATA4'
e = 'DATA105'
dye = [500, 490, 450, 400, 350, 340, 300, 250, 200, 160, 150, 139, 100, 75, 50, 35]

new_values1 = []
new_values2 = []
new_values3 = []
new_values4 = []

for i in tqdm(range(len(file))):
	filename = file.iat[i, 0]
	alelle1 = file.iat[i, 1]
	alelle2 = file.iat[i, 2]

	if filename == 'ROM_12_41_Hos' or filename == 'ROM_12_42_Hos' or filename == 'SAM_12_34_Hos' or filename == 'SAM_12_36_Hos':
		new_values1.append('File not found')
		new_values2.append('File not found')
		new_values3.append('File not found')
		new_values4.append('File not found')
		continue

	if filename != 'POP':
		if filename[0] == 'A':
			filename = filename.replace('A_', '')
		if filename[4] == 'C':
			filename = filename.replace('_CON', '')
		elif filename[4] == 'T':
			filename = filename.replace('_TIG', '')
		abif_file = 'A_' + filename + '.fsa'
		record = SeqIO.read(my_dir+abif_file, 'abi')
		print('\nopening fsa file ({}/{}): {}'.format(i,len(file),abif_file))

		height = []
		index_of_peaks = []
		data1 = list(record.annotations['abif_raw'][b])

		for x in range(find_lower(record.annotations['abif_raw'][e], dye), find_upper(record.annotations['abif_raw'][e], dye)):
			# print("#",end='')
			converted_bp = convert_to_bp(x, record.annotations['abif_raw'][e], dye)
			in_range = converted_bp >= alelle1 - 1.5 and converted_bp <= alelle1 + 1.5
			if in_range:
				index_of_peaks.append(x)
				height.append(data1[x])
			elif converted_bp > alelle1:
				break


		new_values1.append(max(height))
		new_values3.append(index_of_peaks[height.index(max(height))])

		if alelle1 == alelle2:
			new_values2.append(max(height))
			new_values4.append(index_of_peaks[height.index(max(height))])

		else: 
			height = []
			index_of_peaks = []

			for x in range(find_lower(record.annotations['abif_raw'][e], dye), find_upper(record.annotations['abif_raw'][e], dye)):
				# print("#",end='')
				converted_bp = convert_to_bp(x, record.annotations['abif_raw'][e], dye)
				in_range = converted_bp >= alelle2 - 1.5 and converted_bp <= alelle2 + 1.5
				if in_range:
					index_of_peaks.append(x)
					height.append(data1[x])
				elif converted_bp > alelle2:
					break
			new_values2.append(max(height))
			new_values4.append(index_of_peaks[height.index(max(height))])

	else:
		new_values1.append(float('nan'))
		new_values2.append(float('nan'))
		new_values3.append(float('nan'))
		new_values4.append(float('nan'))



# print(file[["Hsc 40"]])

file["Height_column1"] = pd.Series(new_values1)
file["Height_column2"] = pd.Series(new_values2)
file["Index_column3"] = pd.Series(new_values3)
file["Index_column4"] = pd.Series(new_values4)

file.to_csv('/home/bo/PGC/microsat/testdata/training/GetHeight/HSC24-A_Channel2_HeightandIndex.csv')