from findpeaks import findpeaks

def find_lower(data, dye):
	data_105 = list(data)
	i = len(data)
	indexes = findpeaks.findpeaks(data_105, spacing=50, limit=200)
	ind = []
	j = len(indexes) - 1
	k = 0

	while j >= 0:
		if k == 15:
			ind.append(indexes[j])
			break
		ind.append(indexes[j])
		j -= 1
		k += 1

	return ind[len(ind)-1]

def find_upper(data, dye):
	data_105 = list(data)
	i = len(data)
	indexes = findpeaks.findpeaks(data_105, spacing=50, limit=200)
	ind = []
	j = len(indexes) - 1
	k = 0

	while j >= 0:
		if k == 15:
			ind.append(indexes[j])
			break
		ind.append(indexes[j])
		j -= 1
		k += 1

	return ind[0]

def convert_to_bp(alelle, data, LIZ_500):
	data_105 = list(data)
	i = len(data)
	indexes = findpeaks.findpeaks(data_105, spacing=50, limit=200)
	ind = []
	j = len(indexes) - 1
	k = 0

	while j >= 0:
		if k == 15:
			ind.append(indexes[j])
			break
		ind.append(indexes[j])
		j -= 1
		k += 1

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
	indexes = findpeaks.findpeaks(data_105, spacing=50, limit=200)
	ind = []
	j = len(indexes) - 1
	k = 0

	while j >= 0:
		if k == 15:
			ind.append(indexes[j])
			break
		ind.append(indexes[j])
		j -= 1
		k += 1

	for c in range(0, 16):
		if bp > LIZ_500[c]:
			index_pred = ((bp - LIZ_500[c])/((LIZ_500[c-1] - LIZ_500[c])/(ind[c-1] - ind[c]))) + ind[c]
			break

	return index_pred