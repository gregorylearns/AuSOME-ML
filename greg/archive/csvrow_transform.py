"""
This script transforms the current csv formatting of
Filename1   true_peak1	true_peak2
Filename2	true_peak1	true_peak2

into
Filename1	true_peak1
Filename1	true_peak2
Filename2	true_peak1
Filename2	true_peak2

Useful when preparing the training data.
"""
#per row
import pandas as pd

my_dir = "/home/bo/PGC/microsat/testdata/training/GetHeight/"
filename = "Channel1.csv"


def convertrow():
	
	file = pd.read_csv(my_dir+filename)
	i = 0
	filecol = []
	peakcol = []

	while i < len(file):
		if file.iat[i,0] != 'POP':
			filecol.append(file.iat[i,0])
			filecol.append(file.iat[i,0])
			peakcol.append(file.iat[i,1])
			peakcol.append(file.iat[i,2])
		else:
			filecol.append('POP')
			peakcol.append('')
		i +=1

	df = pd.DataFrame(list(zip(filecol,peakcol)),columns=["filename","peakcalls"])
	# print(df)
	df.to_csv(my_dir+"Channel1_transform.csv")
	print("Success!")







def main():
	convertrow()

main()