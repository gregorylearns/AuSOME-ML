#laddermatch.py
#currently this job is done by fragman but we want to not rely on it 
"""
This script is to create a pos wei hei table such as in fragman.
"""
from Bio import SeqIO
from findpeaks import findpeaks
import pandas as pd

test_dir = "/home/bo/PGC/microsat/TestData/Plate1/mini/"
test_file = "A_GUI_12_1.fsa"

def fsatopandas():
	abif_raw = SeqIO.read(test_dir+test_file, 'abi')
	abif_data = pd.DataFrame()


	channels = ["DATA1", "DATA2", "DATA3", "DATA4", "DATA105"]
	Liz_500 = [35, 50, 75, 100, 139, 150, 160, 200, 250, 300, 340, 350, 400, 450, 490, 500]

	for c in channels:
		abif_data[c] = abif_raw.annotations['abif_raw'][c]

	return(abif_data)

