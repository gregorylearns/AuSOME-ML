import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from Bio import SeqIO
from findpeaks import findpeaks as fp
from collections import defaultdict
from time import time

def plot():
	my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
	filename = "A_BOH_12_1.fsa"

	##Load Data from FSA file
	record = SeqIO.read(my_dir+filename,"abi")
	trace = record.annotations['abif_raw']['DATA1']
	
	all_pk = fp.findpeaks(trace, spacing=5,limit=1000)
	all_pk_height = [trace[a] for a in all_pk]
	plt.plot(trace)
	plt.plot(all_pk,all_pk_height,'o')

	seg_ranges = [[x-80,x+40] for x in all_pk_height]

	# segment = np.array(trace[2100:2200])
	# inv_segment = [x * -1 for x in segment]

	# # print(np.trapz(segment[27:75]))
	# fp_spacing = 5
	# fp_limit = 400


	# pk_indexes = fp.findpeaks(segment, spacing=fp_spacing, limit=fp_limit)
	# pki_indexes = fp.findpeaks(inv_segment, spacing=fp_spacing, limit=-fp_limit)
	
	# ## Get the outside bounds of the peaks  
	# pki_index_trim = []
	# peakrange = range(min(pk_indexes), max(pk_indexes))
	
	# for p in range(len(pki_indexes)):
	# 	if pki_indexes[p] in peakrange or pki_indexes[p-1] in peakrange:
	# 		pki_index_trim.append(pki_indexes[p])
	# 	try:
	# 		if pki_indexes[p+1] in peakrange:
	# 			pki_index_trim.append(pki_indexes[p])
	# 	except IndexError:
	# 		pass


	# pk_height = [segment[x] for x in pk_indexes]
	# pki_height = [segment[x] for x in pki_index_trim]
	# #Labels for the graphs
	# pk_height_label = str(len(pk_height))+" high peak(s)"
	# pki_height_label = str(len(pki_height))+" low peak(s)"


	# plt.axhline(y=0, color='k') #x axis line
	# # plt.plot(trace)
	# plt.plot(segment,color='blue') #peak+stutter
	# # plt.plot(inv_segment,color='red') #peak+stutter
	# plt.plot(pk_indexes,pk_height,'o',color='red',markersize=10, label=pk_height_label)
	# plt.plot(pki_index_trim,pki_height,'o',color='green',markersize=10, label=pki_height_label) 
	# plt.title(filename)
	# plt.legend() #show labels
	# plt.show() #print the graph


def visualize_all():
	my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
	test_file = "HSC24-A_Channel2.csv"
	data = pd.read_csv(my_dir+test_file)

	maintrace = defaultdict(list)
	start = time()
	for f in range(len(data)):
		filename = data.iat[f, 0]
		if filename != 'POP':
			if filename[0] == 'A':
				filename = filename.replace('A_', '')
			elif filename[4] == 'C':
				filename = filename.replace('_CON', '')
			elif filename[4] == 'T':
				filename = filename.replace('_TIG', '')
			abif_file = my_dir+ 'A_' + filename + '.fsa'
		else:
			continue
		record = SeqIO.read(abif_file,"abi")
		maintrace['A_'+filename+'.fsa'] = np.array(record.annotations['abif_raw']['DATA105'])
		plt.plot(maintrace['A_'+filename+'.fsa'], alpha=0.1,color='blue')
	print('Initializing {} file(s) took: {:.2f} s'.format(len(data),(time()-start)))
	plt.title("%s to %s "% (data.iat[1, 0],data.iat[-1,0]))
	plt.show()



def main():
	plot()
	# visualize_all()
main()