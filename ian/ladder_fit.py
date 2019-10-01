from findpeaks import findpeaks

def find_lower(data, LIZ_500):
	data_105 = list(data)
	i = len(data)
	indexes = findpeaks.findpeaks(data_105, spacing=35, limit=100)
	ind = []
	j = len(indexes) - 1
	k = 0

	while j >= 0:
		if k == 15:
			ind.append(indexes[j])
			break
		counter = 1
		next_index = j - counter
		del_ratio = (indexes[j] - indexes[next_index])/(LIZ_500[k] - LIZ_500[k+1])
		# print(del_ratio)
		in_range = del_ratio > 8.5 and del_ratio < 13.5
		if in_range:
			ind.append(indexes[j])
			k += 1
			j -= 1
		else:
			while del_ratio < 8.5 or del_ratio > 13.5:
				counter += 1
				next_index = j - counter
				if next_index < 0:
					j -= 1
					counter = 1
					next_index = j - counter
				del_ratio = (indexes[j] - indexes[next_index])/(LIZ_500[k] - LIZ_500[k+1])
			ind.append(indexes[j])
			j = next_index
			k += 1

	if ind[0] == ind[len(ind)-1]:
		ind.pop(len(ind)-1)

	return ind[len(ind)-1]

def find_upper(data, LIZ_500):
	data_105 = list(data)
	i = len(data)
	indexes = findpeaks.findpeaks(data_105, spacing=35, limit=100)
	ind = []
	j = len(indexes) - 1
	k = 0

	while j >= 0:
		if k == 15:
			ind.append(indexes[j])
			break
		counter = 1
		next_index = j - counter
		del_ratio = (indexes[j] - indexes[next_index])/(LIZ_500[k] - LIZ_500[k+1])
		# print(del_ratio)
		in_range = del_ratio > 8.5 and del_ratio < 13.5
		if in_range:
			ind.append(indexes[j])
			k += 1
			j -= 1
		else:
			while del_ratio < 8.5 or del_ratio > 13.5:
				counter += 1
				next_index = j - counter
				if next_index < 0:
					j -= 1
					counter = 1
					next_index = j - counter
				del_ratio = (indexes[j] - indexes[next_index])/(LIZ_500[k] - LIZ_500[k+1])
			ind.append(indexes[j])
			j = next_index
			k += 1

	if ind[0] == ind[len(ind)-1]:
		ind.pop(len(ind)-1)

	return ind[0]

def convert_to_bp(alelle, data, LIZ_500):
	data_105 = list(data)
	i = len(data)
	indexes = findpeaks.findpeaks(data_105, spacing=35, limit=100)
	ind = []
	j = len(indexes) - 1
	k = 0

	# print(indexes)

	while j >= 0:
		if k == 15:
			ind.append(indexes[j])
			break
		counter = 1
		next_index = j - counter
		del_ratio = (indexes[j] - indexes[next_index])/(LIZ_500[k] - LIZ_500[k+1])
		# print(del_ratio)
		in_range = del_ratio > 8.5 and del_ratio < 13.5
		if in_range:
			ind.append(indexes[j])
			k += 1
			j -= 1
		else:
			while del_ratio < 8.5 or del_ratio > 13.5:
				counter += 1
				next_index = j - counter
				if next_index < 0:
					j -= 1
					counter = 1
					next_index = j - counter
				del_ratio = (indexes[j] - indexes[next_index])/(LIZ_500[k] - LIZ_500[k+1])
			ind.append(indexes[j])
			j = next_index
			k += 1
	
	# print(ind)

	for c in range(0, 16):
		if alelle > ind[c] or alelle == ind[c]:
			bp_pred = ((alelle - ind[c])/((ind[c-1] - ind[c])/(LIZ_500[c-1] - LIZ_500[c]))) + LIZ_500[c]
			break
		else:
			bp_pred = 0

	return bp_pred

def convert_to_index(bp, data, LIZ_500):
	data_105 = list(data)
	i = len(data)
	indexes = findpeaks.findpeaks(data_105, spacing=35, limit=100)
	ind = []
	j = len(indexes) - 1
	k = 0

	# print(indexes)

	while j >= 0:
		if k == 15:
			ind.append(indexes[j])
			break
		counter = 1
		next_index = j - counter
		del_ratio = (indexes[j] - indexes[next_index])/(LIZ_500[k] - LIZ_500[k+1])
		print(del_ratio)
		in_range = del_ratio > 8.5 and del_ratio < 13.5
		if in_range:
			ind.append(indexes[j])
			k += 1
			j -= 1
		else:
			while del_ratio < 8.5 or del_ratio > 13.5:
				counter += 1
				next_index = j - counter
				if next_index < 0:
					j -= 1
					counter = 1
					next_index = j - counter
				del_ratio = (indexes[j] - indexes[next_index])/(LIZ_500[k] - LIZ_500[k+1])
				# print(del_ratio)
			ind.append(indexes[j])
			j = next_index
			k += 1

	# print(ind)

	for c in range(0, 16):
		if bp > LIZ_500[c]:
			index_pred = ((bp - LIZ_500[c])/((LIZ_500[c-1] - LIZ_500[c])/(ind[c-1] - ind[c]))) + ind[c]
			break

	return index_pred
