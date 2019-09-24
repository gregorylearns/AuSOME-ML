#ladder convert py
#Greg, 9.20.19 4pm
## To do: efficiently use pandas instad of lists
## To do: support list import for data
import pandas as pd

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

# print(ladder_dataframe())	

def index_bp(ind,DataFrame):
	"""
	Uses the delta value to convert index values into the base pairs value
	"""
	poslist = list(DataFrame[['pos'][0]])
	weilist = list(DataFrame[['wei'][0]])
	dellist = list(DataFrame[['delta'][0]])	
	print("the index is: " + str(ind))
	i = 0
	while i < len(poslist):
		#check if index is equal to the calibrated ladder
		#and return the calibrated bp location
		
		if ind == poslist[i]:
			return(ind)
			#the function ends
			break
		#convert using the formula: bp = ((i - pos(n-1))/delta(n))+wei(n-1)
		elif ind < poslist[i]:
	
			bp_location = (((ind - poslist[i-1])/dellist[i]) + weilist[i-1])
			# print("{} {} {} {}".format(ind,poslist[i-1],dellist[i],weilist[i-1])) # for debugging
			return(bp_location)
			break
		i+=1

# print(index_bp(ind=6390))

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

my_dataframe = ladder_dataframe()


print(bp_index(bp = 206.739,DataFrame=my_dataframe))
print(index_bp(ind=3024,DataFrame=my_dataframe))


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


		





