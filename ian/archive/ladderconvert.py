#ladder convert py
#Greg, 9.20.19 4pm
## To do: efficiently use pandas instad of lists
## To do: support list import for data
import pandas as pd
import simpleconversionscript # for the test array



def index_bp(channel,DataFrame):
	"""
	Uses the delta value to convert index values into the base pairs value
	currently only in batch mode, insert an array here, preferrably a channel 
	"""
	poslist = list(DataFrame[['pos'][0]]) #Because i dont know how to iterate pandas
	weilist = list(DataFrame[['wei'][0]])
	dellist = list(DataFrame[['delta'][0]])	

	output = list()

	counter = 1
	for ind in range(1,len(channel)+1):
		if ind < poslist[0]:
			output.append(0)
		elif ind == poslist[counter]:
			output.append(weilist[counter])
			counter+=1
			if counter == 16: counter = 15 #because the index falls out of range at the last loop
		else:
			bp_location = (((ind - poslist[counter-1])/dellist[counter]) + weilist[counter-1])
			# print("{} {} {} {}".format(c ,poslist[i-1],dellist[i],weilist[i-1])) # debugging
			output.append(bp_location)


	return(output) #a list containing converted index to bp



print(index_bp([3024],DataFrame=ladder_dataframe()))



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


		
# testlist = index_bp(simpleconversionscript.testarray(),DataFrame=ladder_dataframe())
# with open("outputfile.txt","w+") as outputfile:
# 	outputfile.writelines( "%s\n" % item for item in testlist)





