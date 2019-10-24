import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import ladder_fit as lf
from Bio import SeqIO
from findpeaks import findpeaks as fp
from collections import defaultdict
from time import time
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

def filenamePrep(filename):
	if filename != 'POP':
		if filename[0] == 'A':
			filename = filename.replace('A_', '')
		elif filename[4] == 'C':
			filename = filename.replace('_CON', '')
		elif filename[4] == 'T':
			filename = filename.replace('_TIG', '')
		return('A_' + filename + '.fsa')
	else:
		return



def visualize_all(comparisonfile):
	my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
	test_file = "HSC24-A_Channel2.csv"
	data = pd.read_csv(my_dir+test_file)
	currentfile = comparisonfile
	dye = [500, 490, 450, 400, 350, 340, 300, 250, 200, 160, 150, 139, 100, 75, 50, 35]


	record = SeqIO.read(my_dir+currentfile,"abi")
	channeldata = record.annotations['abif_raw']['DATA1']

	plt.subplot(2,1,1)
	mainchanneldata = defaultdict(list)
	start = time()
	for f in range(len(data)):
		filename = filenamePrep(data.iat[f, 0])
		if filename == None:
			continue
		record = SeqIO.read(my_dir+filename,"abi")
		mainchanneldata[filename] = np.array(record.annotations['abif_raw']['DATA1'])
		plt.plot(mainchanneldata[filename], alpha=0.1,color='blue')
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



def plotgraph(directory, filename,peakwindow,threshold=2000):
	filename = filename
	my_dir = directory
	threshold = 500

	#Load Data from FSA file
	record = SeqIO.read(my_dir+filename,"abi")
	channeldata = np.array(record.annotations['abif_raw']['DATA1'])
	ladderdata = np.array(record.annotations['abif_raw']['DATA105'])
	
	#What if the user wants to reset the scan with lower threshold?
	#what if true peak is actually lower than the default 2000 threshold?
	#This while block allows the user to repeat the scanning procedure
	cond = False
	while cond == False:

		all_pk = fp.findpeaks(channeldata, spacing=25,limit=threshold)
		all_pk = [a for a in all_pk 
						if a > int(peakwindow[0]) and a < int(peakwindow[1])]
		all_pk_height = [channeldata[a] for a in all_pk]

		#What if no peaks is detected?
		#This block shows the user the graph and that nothing is detected
		if len(all_pk) == 0:
			print("No peaks found in channel with threshold=%s" % threshold)
			plt.plot(channeldata)
			plt.show()

		print("Peaks detected from channel: %s \n%s\n" % (len(all_pk),all_pk))
		seg_ranges = [[x-80,x+40] for x in all_pk] #Segment Ranges
		
		for i in range(len(seg_ranges)):
			a,b  = seg_ranges[i][0], seg_ranges[i][1]
			segment = np.array(channeldata[a:b])

			# the points
			plt.style.use('seaborn')
			plt.subplot(2,len(seg_ranges),i+1)
			plt.plot(list(range(a,b)),segment,color='blue') #peak+stutter
			plt.title(i+1)
			plt.yticks([])
			plt.ylim(0,max(all_pk_height)+1000)

			
		#bottom
		plt.subplot(2,1,2)
		plt.plot(ladderdata,color='black',alpha=0.3)
		plt.plot(channeldata)
		plt.plot(all_pk,all_pk_height,'o',
					color='red',markersize=5,label="Suggested Peaks")
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
				print("Invalid input")
			else:
				cond = True #condition is fulfulled
				break


		print("Please close graph to continue.....")
		plt.show()
		
	#figure out a way to move these to the top
	height = [channeldata[h] for h in all_pk]
	seg_area = [np.trapz(channeldata[s[0]:s[1]]) for s in seg_ranges]
	sel_peaks = [p-1 for p in sel_peaks]

	not_height = [height[i] for i in range(len(height)) if i not in sel_peaks]
	not_seg_area = [seg_area[i] for i in range(len(seg_area)) if i not in sel_peaks]
	not_sel_peaks = [all_pk[i] for i in range(len(all_pk)) if i not in sel_peaks]

	height = [height[i] for i in range(len(height)) if i in sel_peaks]
	seg_area = [seg_area[i] for i in range(len(seg_area)) if i in sel_peaks]
	sel_peaks = [all_pk[p] for p in sel_peaks]


	pk_area = [np.trapz(channeldata[Peakboundaries(channeldata,i)[0]:Peakboundaries(channeldata,i)[1]])
		for i in sel_peaks]

	pk_area_not = [np.trapz(channeldata[Peakboundaries(channeldata,i)[0]:Peakboundaries(channeldata,i)[1]])
		for i in not_sel_peaks]

	stu_area = [seg_area[i] - pk_area[i] for i in range(len(seg_area))]
	stu_area_not = [not_seg_area[i] - pk_area_not[i] for i in range(len(not_seg_area))]

	"""
	filename = Name of current file
	sel_peaks = Indexes of user-selected peaks
	height, area = height and area of the user-selected peaks
	not_sel_peaks = indexes of the not-selected peaks
	not_height, not_area = height and area of the nonselected peaks
	"""
	return([filename, sel_peaks,height,seg_area,pk_area,stu_area,not_sel_peaks,not_height,not_seg_area,pk_area_not,stu_area_not])


def ROCCurveplot(model,x_test,y_test,y_train):
	probs = model.predict_proba(x_test)
	probs = probs[:,1]

	fpr, tpr, thresholds = roc_curve(y_test, probs)

	auc = roc_auc_score(y_test,probs)
	print(f'AUC: {auc:.5f}')

	plt.style.use('seaborn')
	plt.plot([0,1], [0,1], '--', color='Purple', alpha=0.35)
	# plt.fill([0,0.4,1], [0,0.4,1], color='Purple', alpha=0.65)
	plt.plot(fpr, tpr, color='Purple', label=f"AUC: {auc:.4f}")
	# plt.fill(fpr, tpr, color='Purple', alpha=0.65)
	# plt.title('ROC Curve', fontsize=15)
	# plt.text(0.6, 0.3, f'AUC: {round(auc, 5)}', fontweight='bold')
	plt.legend(loc="lower right")
	plt.xlabel('False Positive Rate', fontsize=10)
	plt.ylabel('True Positive Rate', fontsize=10)
	plt.show()



def linearRegPredict():
	"""
	Machine learning predictive model.
	"""
	file = pd.read_pickle("Channel1_mini_areamethod_result.pk1")
	score, area, height, pk_area, stu_area = [], [], [], [], []
	# file.to_csv("test2.csv")

	# Two for loops because the two are not equal in length
	for i in range(len(file.iloc[:,1])):
		score.extend([1 for j in range(len(file.iat[i,1]))])
		height.extend([j for j in file.iat[i,2]])
		area.extend([j for j in file.iat[i,3]])
		pk_area.extend([j for j in file.iat[i,4]])
		stu_area.extend([j for j in file.iat[i,5]])

	for i in range(len(file.iloc[:,6])):
		score.extend([0 for j in range(len(file.iat[i,6]))])
		height.extend([j for j in file.iat[i,7]])
		area.extend([j for j in file.iat[i,8]])
		pk_area.extend([j for j in file.iat[i,9]])
		stu_area.extend([j for j in file.iat[i,10]])


	df = pd.DataFrame(list(zip(score,height,area,pk_area,stu_area))
		,columns=["score","height","area","peakarea","stutterarea"])
	print(df)

	x_train, x_test, y_train, y_test = train_test_split(df,score,test_size=0.25)

	# logregression
	logmodel = LogisticRegression()
	logmodel.fit(x_train, y_train)

	pred = logmodel.predict(x_test)
	print(f'\nLog model score: {logmodel.score(x_test,y_test):5f}\n')
	print(classification_report(y_test,pred))


	ROCCurveplot(logmodel,x_test,y_test,y_train)

	# plt.plot(x_train,y_train,'o',color='red')
	# plt.plot(x_train, logmodel.predict(x_train))
	# plt.show()

	# print(np.corrcoef(,d_peaks_h)[1,0])

	return()



def Peakboundaries(channel,peak):
	"""
	This function takes the peak index and takes the index of its boundaries.
	This will use a sliding window to find the first zero-slope peak/dip on
	the left or right part of the peak.
	Input: index of peak
	Output: left boundary index
	"""
	leftbound = peak
	rightbound= peak

	dipFound = False
	while dipFound == False:
		slope = (channel[leftbound-1]-channel[leftbound])/((leftbound-1)-leftbound)
		if slope <= 0:
			dipFound = True
			leftbound += 1
		leftbound -= 1

	
	dipFound = False
	while dipFound == False:
		slope = (channel[rightbound+1]-channel[rightbound])/((rightbound+1)-rightbound)
		if slope >= 0:
			dipFound = True
			rightbound -= 1
		rightbound += 1

	return(leftbound,rightbound)







def main():
	filename = "A_BOH_12_12.fsa"
	directory="/home/bo/PGC/microsat/testdata/training/GetHeight/"
	filecsv = pd.read_csv(directory+"Channel1_mini_areamethod.csv")



	print("This script currently only supports .fsa Files from ABI(R) 3730 Sequencing Machine")
	print("Initializing....")

	window = visualize_all(filename)

	df_labels = ["filename","selpeaks","selheight","selarea","peakarea",
				"stutarea","notpeak","notheight","notarea","notpeakarea","notstuarea"]

	my_df = pd.DataFrame(columns=df_labels)


	print(len(filecsv))
	for i in range(len(filecsv)):
		filename = filenamePrep(filecsv.iat[i, 0])
		if filename == None:
			continue
		print(f"Training data, {i+1}/{range(len(filecsv))} files")
		array = plotgraph(directory,filename,window)
		my_df = my_df.append(pd.Series(array,my_df.columns),ignore_index=True)
		print(my_df)
	colname = trainingdata.pop(0)
	# df = pd.DataFrame(trainingdata,columns=colname, dtype=int)
	# my_df.to_pickle("Channel1_mini_areamethod_result2.pk1")

	# plotgraph(directory,filename,window)
main()
# linearRegPredict()

