import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from Bio import SeqIO
from findpeaks import findpeaks

def main():
	my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
	record = SeqIO.read(my_dir+"A_BOH_12_1.fsa","abi")

	trace = record.annotations['abif_raw']['DATA1']
	area = np.array(trace[2100:2200])

	print(np.trapz(area[27:75]))

	indexes = findpeaks.findpeaks(area, spacing=5, limit=250)
	index_height = [area[x] for x in indexes]

	print(indexes)
	print("index height is %s" % index_height)
	print(area[34])
	print(area[58])

	plt.axhline(y=0, color='k')
	plt.plot(area,color='blue')
	plt.plot(indexes,index_height,'o-',color='red')
	plt.show()


main()