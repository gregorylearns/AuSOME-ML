import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from Bio import SeqIO
from findpeaks import findpeaks as fp
from collections import defaultdict
from time import time

def plotgraph():
	my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
	filename = "A_COR_12_2_Hos.fsa"

	#Load Data from FSA file
	record = SeqIO.read(my_dir+filename,"abi")
	channeldata = record.annotations['abif_raw']['DATA4']
	
	all_pk = fp.findpeaks(channeldata, spacing=5,limit=2000)
	all_pk_trim = [a for a in all_pk 
					if a > 1500]

	all_pk_height = [channeldata[a] for a in all_pk_trim]
	# plt.plot(channeldata)

	print("Peaks detected from channel:\n%s\n" % all_pk_trim)

	seg_ranges = [[x-80,x+40] for x in all_pk_trim]
	

	for i in range(len(seg_ranges)):

		a = seg_ranges[i][0]
		b = seg_ranges[i][1]
		
		print("a= %s b=%s " % (a,b))		

		segment = np.array(channeldata[a:b])
		inv_segment = [x * -1 for x in segment]

		# print(np.trapz(segment[27:75]))
		fp_spacing = 5
		fp_limit = 400


		pk_indexes = fp.findpeaks(segment, spacing=fp_spacing, limit=fp_limit)
		pki_indexes = fp.findpeaks(inv_segment, spacing=fp_spacing, limit=-fp_limit)
		
		## Get the outside bounds of the peaks  
		pki_index_trim = []
		peakrange = range(min(pk_indexes), max(pk_indexes))
		
		for p in range(len(pki_indexes)):
			if pki_indexes[p] in peakrange or pki_indexes[p-1] in peakrange:
				pki_index_trim.append(pki_indexes[p])
			try:
				if pki_indexes[p+1] in peakrange:
					pki_index_trim.append(pki_indexes[p])
			except IndexError:
				pass

		pki_index_trim = list(dict.fromkeys(pki_index_trim))

		### end for calling and cleaning outside bounds of the peaks


		pk_height = [segment[x] for x in pk_indexes]
		pki_height = [segment[x] for x in pki_index_trim]
		#Labels for the graphs
		pk_height_label = str(len(pk_height))+" high peak(s)"
		pki_height_label = str(len(pki_height))+" low peak(s)"

		#
		# the points
		plt.subplot(2,len(seg_ranges),i+1)
		plt.plot(pk_indexes,pk_height,'o',color='red',markersize=10, label=pk_height_label)
		plt.plot(pki_index_trim,pki_height,'o',color='green',markersize=10, label=pki_height_label) 
		plt.plot(segment,color='blue') #peak+stutter
		plt.ylim(0,max(all_pk_height)+1000)
		plt.axhline(y=0, color='k') #x axis line
		plt.title("{} to {}".format(a,b))
		plt.legend() #show labels	
		
		#

	#bottom
	plt.subplot(2,1,2)
	plt.plot(channeldata)
	plt.plot(all_pk_trim,all_pk_height,'+',color='black',markersize=5,label="Peaks")
	plt.ylim(0,max(all_pk_height)+1000)
	plt.xlim(500,7000)
	for i in range(len(seg_ranges)):
		plt.axvspan(seg_ranges[i][0], seg_ranges[i][1], color='m', alpha=0.5)
	plt.axhline(y=0, color='k') #x axis line
	plt.title(filename)


	
	plt.show() #print the graph


def visualize_all():
	my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
	test_file = "HSC24-A_Channel2.csv"
	data = pd.read_csv(my_dir+test_file)

	mainchanneldata = defaultdict(list)
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
		mainchanneldata['A_'+filename+'.fsa'] = np.array(record.annotations['abif_raw']['DATA1'])
		plt.plot(mainchanneldata['A_'+filename+'.fsa'], alpha=0.1,color='blue')
	print('Initializing {} file(s) took: {:.2f} s'.format(len(data),(time()-start)))
	plt.title("%s to %s "% (data.iat[1, 0],data.iat[-1,0]))
	plt.show()


def getarea():
	my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
	test_file = "HSC24-A_Channel2.csv"
	data = pd.read_csv(my_dir+test_file)
	


	mainchanneldata = defaultdict(list)

	return()




def main():
	plotgraph()
	# visualize_all()
main()