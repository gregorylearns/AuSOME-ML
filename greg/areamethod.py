import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from Bio import SeqIO
from findpeaks import findpeaks as fp
from collections import defaultdict
from time import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def plotgraph(directory, filename,peakwindow,threshold=2000):
	filename = filename
	my_dir = directory
	threshold = threshold

	#Load Data from FSA file
	record = SeqIO.read(my_dir+filename,"abi")
	channeldata = np.array(record.annotations['abif_raw']['DATA1'])
	ladderdata = np.array(record.annotations['abif_raw']['DATA105'])
	
	#What if the user wants to reset the scan with lower threshold?
	#what if true peak is actually lower than the default 2000 threshold?
	#This while block allows the user to repeat the scanning procedure
	cond = False
	while cond == False:

		all_pk = fp.findpeaks(channeldata, spacing=30,limit=threshold)
		all_pk_trim = [a for a in all_pk 
						if a > int(peakwindow[0]) and a < int(peakwindow[1])]
		all_pk_height = [channeldata[a] for a in all_pk_trim]

		#What if no peaks is detected?
		#This block shows the user the graph and that nothing is detected
		if len(all_pk_trim) == 0:
			print("No peaks found in channel with threshold=%s" % threshold)
			plt.plot(channeldata)
			plt.show()


		print("Peaks detected from channel: %s \n%s\n" % (len(all_pk_trim),all_pk_trim))
		seg_ranges = [[x-80,x+40] for x in all_pk_trim] #Segment Ranges
		

		for i in range(len(seg_ranges)):

			a,b  = seg_ranges[i][0], seg_ranges[i][1]

			segment = np.array(channeldata[a:b])
			### inner peaks boundaries depreciated code below
			# the points
			plt.subplot(2,len(seg_ranges),i+1)

			plt.plot(list(range(a,b)),segment,color='blue') #peak+stutter
			# plt.xlim(a,b)
			plt.ylim(0,max(all_pk_height)+1000)
			plt.axhline(y=0, color='k') #x axis line
			plt.title("{} to {}".format(a,b))
			plt.legend() #show labels	
			
			#

		#bottom
		plt.subplot(2,1,2)
		plt.plot(ladderdata,color='black',alpha=0.3)
		plt.plot(channeldata)
		plt.plot(all_pk_trim,all_pk_height,'+',
					color='black',markersize=5,label="Suggested Peaks")
		plt.ylim(0,max(all_pk_height)+1000)
		plt.xlim(500,7000)

		for i in range(len(seg_ranges)):
			plt.axvspan(seg_ranges[i][0], seg_ranges[i][1], color='m', alpha=0.5)

		plt.axvspan(0,peakwindow[0], 
					color ='black',alpha=0.3,label="Excluded from peak search")
		plt.axvspan(int(peakwindow[1]), len(channeldata),color ='black', alpha=0.3)
		plt.axhline(y=0, color='k') #x axis line
		plt.title(filename)
		plt.legend() #show labels	
		plt.show(block=False) #print the graph

		print("%s potential peaks detected. Please select peaks " % len(seg_ranges),end='')
		print("separated by commas. \ne.g: 1,2 (heterozygous) or 1,1 (homozygous)\n")
		
		print("[0] -> Repeat scan with lower threshold")
		for i in range(len(seg_ranges)):
			print("[{}] -> {}".format(i+1,seg_ranges[i]))


		#Asks for user input and select peaks to choose
		#Idea: add option to repeat findpeaks or manual [0] if desired peak is not detected.

		while True:
			sel_peaks = str(input("\n>")).split(',')
			sel_peaks = [int(p) for p in sel_peaks]
			if len(sel_peaks) == 1 and sel_peaks[0] == 0:
				#not all thres is detected, repeat scan
				threshold -= 500
				print("Repeating scan with lowered threshold (-500)")
				break
			elif len(sel_peaks) > len(seg_ranges) or min(sel_peaks) < 0 or max(sel_peaks) > len(seg_ranges):
				# print("len(sp):{} > len(sr):{} or min(sp):{} < 0 or max(sp):{} > len(sel_peaks):{}".format(len(sel_peaks),len(seg_ranges),min(sel_peaks),max(sel_peaks),len(sel_peaks)))
				print("Invalid input")
			else:
				if len(sel_peaks) == 1 and sel_peaks[0] != 0:
					sel_peaks = [sel_peaks[0], sel_peaks[0]]
				cond = True #condition is fulfulled
				break


		print("Please close graph to continue.....")
		plt.show()
		

	sel_peaks = [p-1 for p in sel_peaks]
	height = [channeldata[h] for h in all_pk_trim]
	area = [np.trapz(channeldata[s[0]:s[1]]) for s in seg_ranges]
	# area = [i for i in range(len(seg_ranges))]
	#Returns Filename, list index of user selected peaks, threshold, List of peaks in threshold, area of segment, height of segment 
	print([filename, sel_peaks,threshold,all_pk_trim,height,area])
	return([filename, sel_peaks, threshold,all_pk_trim,height,area])



def visualize_all(filename):
	my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
	test_file = "HSC24-A_Channel2.csv"
	data = pd.read_csv(my_dir+test_file)
	currentfile = filename

	record = SeqIO.read(my_dir+filename,"abi")
	channeldata = record.annotations['abif_raw']['DATA1']


	plt.subplot(2,1,1)
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
	
	#bottom plot
	plt.subplot(2,1,2)
	plt.plot(channeldata)
	plt.title(currentfile)
	plt.show(block=False)

	while True:
		window = (str(input("Please insert search window ('x,y') or 'all': ")).split(','))
		if len(window) == 2:
			break
		elif window[0].lower() == 'all':
			window = [0,7000]
			break

	print("\nPlease close graph to continue.....\n")
	plt.show()


	return(window)




def linearRegPredict():
	file = pd.read_pickle("Channel1_mini_areamethod_result.pk1")
	userpeaks, d_peaks, d_peaks_h, d_peaks_a = [], [], [], []
	print(file)

	##Get 
	for i in range(len(file.iloc[:,1])):
		for j in range(len(file.iat[i,1])):
			indexinlist = file.iat[i,1][j]
			userpeaks.append(indexinlist)
			d_peaks.append(file.iat[i,3][indexinlist])
			d_peaks_h.append(file.iat[i,4][indexinlist])
			d_peaks_a.append(file.iat[i,5][indexinlist])

	# print(userpeaks)
	# print(d_peaks)
	# print(d_peaks_h)
	# print(d_peaks_a)

	x_train, x_test, y_train, y_test = train_test_split(d_peaks_h,d_peaks_a,test_size=0.25)

	linearRegressor = LinearRegression()
	# d_peaks_a = np.array(d_peaks_a).reshape(-1,1)
	# d_peaks_h = np.array(d_peaks_h).reshape(-1,1)
	linearRegressor.fit(x_train, y_train)
	print(linearRegressor.score(x_test,y_test))

	print(np.corrcoef(d_peaks_a,d_peaks_h)[1,0])
	plt.scatter(d_peaks_h, d_peaks_a)
	plt.show()



	return()






def main():
	filename = "A_COR_12_13_Hos.fsa"
	directory="/home/bo/PGC/microsat/testdata/training/GetHeight/"
	filecsv = pd.read_csv(directory+"Channel1_mini_areamethod.csv")



	print("This script currently only supports .fsa Files from ABI(R) 3730 Sequencing Machine")
	print("Initializing....")

	window = visualize_all(filename)

	trainingdata = [["filename","userPeaks","threshold","detectedPeaks","detectedPeaksHeight","detectedPeaksArea"]]

	for i in range(len(filecsv)):
		filename = filecsv.iat[i, 0]
		if filename != 'POP':
			if filename[0] == 'A':
				filename = filename.replace('A_', '')
			elif filename[4] == 'C':
				filename = filename.replace('_CON', '')
			elif filename[4] == 'T':
				filename = filename.replace('_TIG', '')
			abif_file = 'A_' + filename + '.fsa'

		print("Training data, {}/10 files".format(i))
		array = plotgraph(directory,abif_file,window)
		trainingdata.append(array)

	colname = trainingdata.pop(0)
	df = pd.DataFrame(trainingdata,columns=colname, dtype=int)
	df.to_pickle("Channel1_mini_areamethod_result.pk1")

# main()
linearRegPredict()













#####
##### Inner peaks and boundaries
			# inv_segment = [x * -1 for x in segment]

			# # print(np.trapz(segment[27:75]))
			# fp_spacing = 15
			# fp_limit = 100


			# pk_indexes = fp.findpeaks(segment, spacing=fp_spacing, limit=fp_limit)
			# pki_indexes = fp.findpeaks(inv_segment, spacing=fp_spacing, limit=-fp_limit)
			
			# # pk_indexes = [a + p for p in pk_indexes]
			# # pki_indexes = [a + p for p in pki_indexes]

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

			# pki_index_trim = list(dict.fromkeys(pki_index_trim))

			# ### end for calling and cleaning outside bounds of the peaks


			# pk_height = [segment[x] for x in pk_indexes]
			# pki_height = [segment[x] for x in pki_index_trim]
			# #Labels for the graphs
			# pk_height_label = str(len(pk_height))+" high peak(s)"
			# pki_height_label = str(len(pki_height))+" low peak(s)"

##### 
##### Plotting

			# #plot the red peaks
			# plt.plot([a + p for p in pk_indexes],pk_height,
			# 	'o',color='red',markersize=10, label=pk_height_label)
			# #plot the green out-bound bottom peaks
			# plt.plot([a + p for p in pki_index_trim],
			# 	pki_height,'o',color='green',markersize=10, label=pki_height_label) 