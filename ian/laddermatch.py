#laddermatch.py
#currently this job is done by fragman but we want to not rely on it 
"""
This script is to create a pos wei hei table such as in fragman.
"""
from Bio import SeqIO
import findpeaks
import pandas as pd

test_dir = "/home/bo/PGC/microsat/TestData/Plate1/mini/"
test_file = "A_GUI_12_1.fsa"

test_dir_cor = "/home/bo/PGC/microsat/TestData/BRC_Kim_Plate_4_190613/"
test_file_cor = "A_COR_12_1_Hos.fsa"

def fsatopandas():
	"""
	Reads the fsa file using Biopython and stores the raw data of the channels 
	to abif_data, a pandas dataframe.
	DATA1-4 = Raw data of the channels where the peaks are
	DATA105 = the LIZ_500 GeneScan standard peaks
	for more information on the abif file system
	https://projects.nfstc.org/workshops/resources/articles/ABIF_File_Format.pdf
	"""
	abif_raw = SeqIO.read(test_dir_cor+test_file_cor, 'abi')
	abif_data = pd.DataFrame()


	channels = ["DATA1", "DATA2", "DATA3", "DATA4", "DATA105"]


	for c in channels:
		abif_data[c] = abif_raw.annotations['abif_raw'][c]

	return(abif_data)

abif_data = fsatopandas()


def laddermatch():
	"""
	Very similar to ladderconvert.ladder_dataframe function. That function takes
	CSV file generated by FRAGMAN(R package), and creates a pd dataframe of the 
	csv as well as the delta values.

	Delta is the ratio of the changes in index('pos')/changes in stdard('wei')
	Delta(ratio) is useful in the next two functions that converts index to bp 
	and vice versa.
	"""
	liz_500 = [35, 50, 75, 100, 139, 150, 160, 200, 250, 300, 340, 350, 400, 450, 490, 500]
	data_105 = list(abif_data["DATA105"])

	#gives different results, update parameters or the findpeaks function
	ind_pos = list(findpeaks.findpeaks(data_105, spacing=50, limit=200))
	# hei = [data_105[x] for x in ind_pos] #no need to ouput on table, just a nice to have
	# print(hei)
	for i in range(len(ind_pos) - len(liz_500)):
		"""
		Remove the first n elements so that index length = liz length, with the 
		end of the list as the standard
		"""
		ind_pos.pop(0)

	delta = []
	i=0
	while i < len(ind_pos):
	    if i == 0:
	        i +=1
	        delta.append(0)
	        continue 
	    d = (ind_pos[i]-ind_pos[i-1])/(liz_500[i]-liz_500[i-1])
	    delta.append(d)
	    i +=1

	#exactly the same with the output of ladderconvert.ladder_dataframe function
	deltaframe = pd.DataFrame(list(zip(ind_pos,liz_500,delta)),columns = ['pos','wei','delta'])
	return(deltaframe)

print(laddermatch())

# print(laddermatch())