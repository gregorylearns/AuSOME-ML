#slopefinder
import matplotlib.pyplot as plt
from Bio import SeqIO
from findpeaks import findpeaks as fp

a = 3350
b = 3450

def unduplicateuserpeaks():
	#stupid function
	filename = "Channel1_mini_areamethod_result"
	df = pd.read_pickle(filename+".pk1")
	print(df)
	newuserpeaks = []
	userpeaks = df.iloc[:,1]
	for i in range(len(userpeaks)):
		if userpeaks[i][0] == userpeaks[i][1]:
			newuserpeaks.append([userpeaks[i][0]])
		else:
			newuserpeaks.append(userpeaks[i])
	print(userpeaks)
	print(newuserpeaks)

	df.drop("UserPeaks",axis=1,inplace=True)
	df.insert(1,"UserPeaks",newuserpeaks)
	df.to_pickle(filename+"_unduplicated.pk1")

def leftwarddip(channel,peak):
	peak = peak[0] + a

	dipFound = False
	while dipFound == False:
		slope = (channel[peak-1]-channel[peak])/((peak-1)-peak)

		if slope <= 0:
			dipFound = True
			plt.scatter(peak- a, channeldata[peak],color='red')
			peak += 1

		peak -= 1
	return(peak)

def rightwarddip(channel,peak):
	peak = peak[0] + a
	
	dipFound = False
	while dipFound == False:
		slope = (channel[peak+1]-channel[peak])/((peak+1)-peak)
		if slope >= 0:
			dipFound = True
			plt.scatter(peak- a, channeldata[peak],color='red')
			peak -= 1

		peak += 1
	return(peak)

currentfile = "A_BOH_12_12.fsa"
my_dir="/home/bo/PGC/microsat/testdata/training/GetHeight/"
record = SeqIO.read(my_dir+currentfile,"abi")
channeldata = record.annotations['abif_raw']['DATA1']
smol_test = channeldata[a:b]

all_peaks = fp.findpeaks(smol_test,spacing=5,limit=1000)
print(all_peaks)


print(leftwarddip(channeldata,all_peaks))
print(rightwarddip(channeldata,all_peaks))

plt.scatter(all_peaks,[channeldata[3350 + i] for i in all_peaks])
plt.plot(smol_test,'-o',markersize=4)
plt.show()


