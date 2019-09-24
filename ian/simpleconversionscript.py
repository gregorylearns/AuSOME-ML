#simple conversion script. just needed an array for testing ladderconvert.py
from Bio import SeqIO
from collections import defaultdict


directory = "/home/bo/PGC/microsat/TestData/Plate1/mini/"
file = 'A_GUI_12_1.fsa'

def testarray():
	record = SeqIO.read(directory+file, 'abi')
	channels = ['DATA1', 'DATA2', 'DATA3', 'DATA4', 'DATA105']
	trace = defaultdict(list)


	for c in channels:
		trace[c] = record.annotations['abif_raw'][c]
	return(trace['DATA1'])

