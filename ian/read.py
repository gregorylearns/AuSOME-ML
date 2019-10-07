from Bio import SeqIO
from matplotlib import pyplot as plt
from collections import defaultdict
import numpy as np
import pandas as pd
import math
from ladder_fit import convert_to_bp, convert_to_index, find_lower, find_upper
from findpeaks import findpeaks as fp

# <<<<<<< HEAD
# <<<<<<< HEAD
# my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
# file = pd.read_csv(my_dir+'HSC24-A_Channel2_Mini.csv')
# =======
# file = pd.read_csv('Channel1_Data.csv')
# >>>>>>> f9afbe3... updated read.py and added Hsc40.csv
# =======
file = pd.read_csv('Channel1_Data_Normalized.csv')
# >>>>>>> 4859ffb... added datasets and updated AuSOME.py
a = 'DATA1'
b = 'DATA2'
c = 'DATA3'
d = 'DATA4'
e = 'DATA105'
dye = [500, 490, 450, 400, 350, 340, 300, 250, 200, 160, 150, 139, 100, 75, 50, 35]

# <<<<<<< HEAD
# new_values1 = []
# new_values2 = []
# new_values3 = []
# new_values4 = []

# new_v_area1 = []
# new_v_area2 = []

# for i in tqdm(range(len(file))):
# =======
# new_values1 = []
# new_values2 = []
# new_values3 = []
# new_values4 = []
area_of_peaks = []
label = []
file_name = []
number_of_peaks = []
length_in_bp = []
noise_count = 0

for i in range(len(file)):
# >>>>>>> f9afbe3... updated read.py and added Hsc40.csv
	filename = file.iat[i, 0]
	alelle1 = file.iat[i, 1]
	alelle2 = file.iat[i, 2]

	if filename == 'ROM_12_41_Hos' or filename == 'ROM_12_42_Hos' or filename == 'SAM_12_34_Hos' or filename == 'SAM_12_36_Hos':
		# new_values1.append('File not found')
		# new_values2.append('File not found')
		# new_values3.append('File not found')
		# new_values4.append('File not found')
		continue

	if filename != 'POP':
		if filename[0] == 'A':
			filename = filename.replace('A_', '')
		if filename[4] == 'C':
			filename = filename.replace('_CON', '')
		elif filename[4] == 'T':
			filename = filename.replace('_TIG', '')
		abif_file = 'A_' + filename + '.fsa'
		record = SeqIO.read(abif_file, 'abi')
		print('\nopening fsa file ({}/{}): {}'.format(i,len(file),abif_file))

		# height = []
		# index_of_peaks = []
		# data1 = list(record.annotations['abif_raw'][a])

		# for x in range(find_lower(record.annotations['abif_raw'][e], dye), find_upper(record.annotations['abif_raw'][e], dye)):
		# 	# print("#",end='')
		# 	converted_bp = convert_to_bp(x, record.annotations['abif_raw'][e], dye)
		# 	in_range = converted_bp >= alelle1 - 1.5 and converted_bp <= alelle1 + 1.5
		# 	if in_range:
		# 		index_of_peaks.append(x)
		# 		height.append(data1[x])
		# 	elif converted_bp > alelle1:
		# 		break
		# new_values1.append(max(height))
		# new_values3.append(index_of_peaks[height.index(max(height))])

		# height = []
		# index_of_peaks = []

		# for x in range(find_lower(record.annotations['abif_raw'][e], dye), find_upper(record.annotations['abif_raw'][e], dye)):
		# 	# print("#",end='')
		# 	converted_bp = convert_to_bp(x, record.annotations['abif_raw'][e], dye)
		# 	in_range = converted_bp >= alelle2 - 1.5 and converted_bp <= alelle2 + 1.5
		# 	if in_range:
		# 		index_of_peaks.append(x)
		# 		height.append(data1[x])
		# 	elif converted_bp > alelle2:
		# 		break
		# new_values2.append(max(height))
		# new_values4.append(index_of_peaks[height.index(max(height))])



		index_min = find_lower(record.annotations['abif_raw'][e], dye)
		index_max = find_upper(record.annotations['abif_raw'][e], dye)
		data = record.annotations['abif_raw'][a]

		height = []
		index_of_peaks = []
		for x in range(index_min, index_max):
			# print("#",end='')
			converted_bp = convert_to_bp(x, record.annotations['abif_raw'][e], dye)
			in_range = converted_bp >= alelle1 - 1.5 and converted_bp <= alelle1 + 1.5
			if in_range:
				index_of_peaks.append(x)
				height.append(data[x])
			elif converted_bp > alelle1+1.5:
				break
		alelle1_index = index_of_peaks[height.index(max(height))]

# <<<<<<< HEAD
# 		ind = index_of_peaks[height.index(max(height))]

# 		new_values1.append(max(height))
# 		new_values3.append(ind)
# 		new_v_area1.append(np.trapz(data1[ind-80:ind+40]))


		# if alelle1 == alelle2:
		# 	new_values2.append(max(height))
		# 	new_values4.append(index_of_peaks[height.index(max(height))])

		# else: 

		if alelle1 != alelle2:

			height = []
			index_of_peaks = []
			for x in range(index_min, index_max):
			# print("#",end='')
				converted_bp = convert_to_bp(x, record.annotations['abif_raw'][e], dye)
				in_range = converted_bp >= alelle2 - 1.5 and converted_bp <= alelle2 + 1.5
				if in_range:
					index_of_peaks.append(x)
					height.append(data[x])
				elif converted_bp > alelle2+1.5:
					break

			alelle2_index = index_of_peaks[height.index(max(height))]

			if alelle2_index > alelle1_index:
				if alelle1_index+80>=alelle2_index:
					two_peaks = True
				else:
					two_peaks = False
			else:
				if alelle1_index-80<=alelle2_index:
					two_peaks = True
				else:
					two_peaks = False

		all_peaks = fp.findpeaks(data, spacing=15, limit=100)

		for i in range(len(all_peaks)-1):
			lower = all_peaks[i] - 80
			upper = all_peaks[i] + 20
			if lower < index_min or upper > index_max:
				continue

			if noise_count > 2320:
				if alelle1 != alelle2:
					if all_peaks[i] == alelle1_index or all_peaks[i] == alelle2_index:
						file_name.append(filename)
						area_of_peaks.append(np.trapz(data[lower:upper]))
						number_of_peaks.append(len(fp.findpeaks(data[lower:upper], spacing=5,limit=50)))
						length_in_bp.append(round(convert_to_bp(all_peaks[i], record.annotations['abif_raw'][e], dye)))	
					else:
						continue
				elif alelle1 == alelle2:
					if all_peaks[i] == alelle1_index:
						file_name.append(filename)
						area_of_peaks.append(np.trapz(data[lower:upper]))
						number_of_peaks.append(len(fp.findpeaks(data[lower:upper], spacing=5,limit=50)))
						length_in_bp.append(round(convert_to_bp(all_peaks[i], record.annotations['abif_raw'][e], dye)))
					else:
						continue
			else:
				file_name.append(filename)
				area_of_peaks.append(np.trapz(data[lower:upper]))
				number_of_peaks.append(len(fp.findpeaks(data[lower:upper], spacing=5,limit=50)))
				length_in_bp.append(round(convert_to_bp(all_peaks[i], record.annotations['abif_raw'][e], dye)))


			if alelle1 != alelle2:
				if two_peaks == True:
					if all_peaks[i] == alelle1_index or all_peaks[i] == alelle2_index:
						label.append(1)
					else:
						label.append(0)
						noise_count += 1
				elif two_peaks == False:
					if all_peaks[i] == alelle1_index or all_peaks[i] == alelle2_index:
						label.append(1)
					else:
						label.append(0)
						noise_count += 1
			elif alelle1==alelle2:
				# print(alelle1_index)
				# print(all_peaks[i])
				if all_peaks[i] == alelle1_index:
					label.append(1)
				else:
					label.append(0)
					noise_count += 1

	else:
		continue
		# new_values1.append(float('nan'))
		# new_values2.append(float('nan'))
		# new_values3.append(float('nan'))
		# new_values4.append(float('nan'))
# >>>>>>> f9afbe3... updated read.py and added Hsc40.csv



# print(file[["Hsc 40"]])
dataset = {'Filename': file_name, 'Label': label, 'Area': area_of_peaks, 'No. of peaks': number_of_peaks, 'Length': length_in_bp}

df = pd.DataFrame(dataset, columns=['Filename', 'Label', 'Area', 'No. of peaks', 'Length'])
df.to_csv('Hsc40_Area_NofPeaks_Length_reduced1.csv', index=False)

# <<<<<<< HEAD
# file["Height_column1"] = pd.Series(new_values1)
# file["Height_column2"] = pd.Series(new_values2)
# file["Index_column3"] = pd.Series(new_values3)
# file["Index_column4"] = pd.Series(new_values4)
# file["Area_column1"] = pd.Series(new_v_area1)
# file["Area_column2"] = pd.Series(new_v_area2)

# file.to_csv(my_dir+'HSC24-A_Channel2_Mini_witharea.csv')
# print(my_dir+'HSC24-A_Channel2_Mini_witharea.csv Saved')
# =======
# file["Height_column1"] = pd.Series(new_values1)
# file["Height_column2"] = pd.Series(new_values2)
# file["Index_column3"] = pd.Series(new_values3)
# file["Index_column4"] = pd.Series(new_values4)

# file.to_csv('Height_and_Index.csv')
# >>>>>>> f9afbe3... updated read.py and added Hsc40.csv
