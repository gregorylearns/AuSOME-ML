#directory check

from os.path import exists
import pandas as pd
from tqdm import tqdm

my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
downloads = "/mnt/Win_D/User_Folders/Downloads/"
file = pd.read_csv(my_dir+'HSC20_D_Channel4.csv')
to_check = []

def checkdir():
	for f in range(len(file)):
		filename = file.iat[f, 0]
		if filename != 'POP':
			if filename[0] == 'A':
				filename = filename.replace('A_', '')
			elif filename[4] == 'C':
				filename = filename.replace('_CON', '')
			elif filename[4] == 'T':
				filename = filename.replace('_TIG', '')



		conditional = exists(my_dir+"A_"+filename+".fsa")
		print("{}:".format(f+2),end='') 
		if conditional == False:
			print("* %s" % filename)
			to_check.append(f)
		else:
			print("")
		# print("{}: {} = {}".format(f+2,filename,conditional))

	print(to_check)

def samevalue():
	counter =0
	for f in range(len(file)):
		if file.iat[f, 1] == file.iat[f, 2]:
			print("*",end='')
			counter +=1
		print("{}: {}".format(f+2,"A_"+file.iat[f,0]+".fsa"))
	print(counter)


def main():
	checkdir()
	# samevalue()

main()