#ladder convert py
#Greg, 9.20.19 4pm
## To do: efficiently use pandas instad of lists
## To do: support list import for data
import pandas as pd
import simpleconversionscript

test_dir = "/home/bo/PGC/microsat/TestData/Plate1/mini/"
test_file = "A_GUI_12_1.csv"

def ladder_dataframe(csvdir=test_dir,file=test_file): 
	"""
	Creates a dataframe from the CSV file from fragman, and creates a column named delta.
	Delta is the ratio of the changes in index('pos')/changes in stdard('wei')
	Delta(ratio) is useful in the next two functions that converts index to bp and vice versa.
	"""
	dataframe = pd.read_csv(csvdir+file, delimiter=',')
	#because i dont know how to iterate through panda columns yet && update when I do
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
	return(deltaframe) #returns a table of values that contain 'pos', 'wei', and 'delta'



def index_bp(channel,DataFrame):
	"""
	Uses the delta value to convert index values into the base pairs value
	currently only in batch mode, insert an array here, preferrably a channel 
	"""
	poslist = list(DataFrame[['pos'][0]]) #Because i dont know how to iterate pandas
	weilist = list(DataFrame[['wei'][0]])
	dellist = list(DataFrame[['delta'][0]])	
	print(DataFrame)

	output = list()
	print("the length of channel is %s" % len(channel))

	exact = 1
	for ind in range(1,len(channel)+1):
		if ind < poslist[1]:
			output.append(0)
		elif ind == poslist[exact]:
			output.append(weilist[exact])
			exact+=1
			if exact == 16: exact = 15 #because the index falls out of range at the last loop
		else:
			bp_location = (((ind - poslist[exact-1])/dellist[exact]) + weilist[exact-1])
			# print("{} {} {} {}".format(c ,poslist[i-1],dellist[i],weilist[i-1])) # debugging
			output.append(bp_location)


	print("the length of the output list is: %s" % len(output))
	return(output)


outlist =index_bp(simpleconversionscript.testarray(),DataFrame=ladder_dataframe())
with open("output.txt",'w+') as file:
	file.writelines( "%s\n" % item for item in outlist)
# index_bp(3024,DataFrame=ladder_dataframe())


def bp_index(bp,DataFrame):
	"""
	Uses the delta value to convert base pairs values into the index value
	"""
	poslist = list(DataFrame[['pos'][0]])
	weilist = list(DataFrame[['wei'][0]])
	dellist = list(DataFrame[['delta'][0]])	
	print("the bp is: " + str(bp))
	i = 0
	while i < len(weilist):
		#check if bp is equal to the calibrated ladder
		#and return the calibrated bp location
		# print(i)
		if bp == weilist[i]:
			return(ind)
			#the function ends
			break
		#convert using the formula: in = (bp - wei[i-1]) * delta[i] + poslist[i-1]
		elif bp < weilist[i]:
	
			in_location = ((bp - weilist[i-1]) * dellist[i]) + poslist[i-1]
			# print("{} {} {} {}".format(bp,weilist[i-1],dellist[i],poslist[i-1])) # for debugging
			return(in_location)
			break
		i+=1

# my_dataframe = ladder_dataframe()


# print(bp_index(bp = 206.739,DataFrame=my_dataframe))


##supposed single function method for all
# def bpindexconvert(bp=0,index=0):
# 	#open the data frame
# 	deltaframe = ladder_dataframe()
# 	#check if bp or index has values
# 	#if both has values, return error
# 	#if bp, convert to index, if index convert to bp
# 	if bp > 0 & index > 0:
# 		#print error and break
# 		return()
# 	elif bp > 0:
# 		#convert bp to index
# 		return()
# 	elif index > 0:
# 		#convert index to bp
# 		return()


		





