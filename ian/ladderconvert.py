#ladder convert py
#Greg, 9.20.19 4pm
import pandas as pd

## 
directory = "/home/bo/PGC/microsat/TestData/Plate1/mini/"
filename = "A_GUI_12_1.csv"

def ladder_dataframe(csvdir=directory,file=filename):
	dataframe = pd.read_csv(csvdir+file, delimiter=',')

	#Generate table
	delta = [0]
	for i in range(len(dataframe[['pos'][0]])):
	    delta.append(dataframe[['wei'][0]])

	#because i dont know how to iterate through panda columns yet
	#update when i know how to iterate through panda columns


	pos = list(dataframe[['pos'][0]])
	wei = list(dataframe[['wei'][0]])
	delta = []
	i = 0

	while i < len(pos):
	    if i == 0:
	        i +=1
	        delta.append(0)
	        continue 
	    a= (pos[i]-pos[i-1])/(wei[i]-wei[i-1])
	    delta.append(a)
	    i +=1

	deltaframe = pd.DataFrame(list(zip(pos,wei,delta)),columns = ['pos','wei','delta'])
	return(deltaframe)


print(ladder_dataframe())


def ladder_bpindex_convert(bp=0,index=0):
	deltaframe = ladder_dataframe()
	



	return()