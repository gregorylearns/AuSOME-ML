from sys import argv
from Bio import SeqIO
from matplotlib import pyplot as plt
from collections import defaultdict

def plotfsa(file="A_GUI_12_2.fsa"):
	directory = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
	
	channels = ['DATA1', "DATA2", "DATA3", "DATA4", "DATA105"]
	LIZ_500 = [500, 490, 450, 400, 350, 340, 300, 250, 200, 160, 150, 139, 100, 75, 50, 35]
	Liz_500 = [35, 50, 75, 100, 139, 150, 160, 200, 250, 300, 340, 350, 400, 450, 490, 500]


	record = SeqIO.read(directory+file, 'abi')
	trace = defaultdict(list)

	for c in channels:
		trace[c] = record.annotations['abif_raw'][c]

	# print(record.annotations.keys())

	plt.plot(trace['DATA1'], color='blue')
	plt.plot(trace['DATA2'], color='red')
	plt.plot(trace['DATA3'], color='green')
	plt.plot(trace['DATA4'], color='yellow')
	plt.plot(trace['DATA105'], color='black')

	plt.ylim((0,10000))
	plt.show()

def main():
	plotfsa(file=argv[1])

main()