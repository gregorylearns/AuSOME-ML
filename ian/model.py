import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

file = pd.read_csv('Area_NofPeaks_Length_reduced.csv')

label = []
area = []
no_of_peaks = []
length = []

for i in range(len(file)):
	label.append(file.iat[i, 1])
	area.append(file.iat[i, 2])
	no_of_peaks.append(file.iat[i, 3])
	length.append(file.iat[i, 4])

matrix = [area, no_of_peaks, length]
X = np.column_stack(matrix)
y = label
# one = 0
# zero = 0
# for i in range(len(y)-1):
# 	if y[i] == 1:
# 		one += 1
# 	elif y[i] == 0:
# 		zero += 1
# print(f'Ones: {one}		Zeroes: {zero}')

sm = SMOTE()
X_res, y_res = sm.fit_resample(X, y)

# print(y_res)
# one = 0
# zero = 0
# for i in range(len(y_res)-1):
# 	if y_res[i] == 1:
# 		one += 1
# 	elif y_res[i] == 0:
# 		zero += 1
# print(f'Ones: {one}		Zeroes: {zero}')

X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.25)
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

# scores = []

# for i in range(1, 1000):
# 	print(f'Getting accuracy score for n_estimators = {i}...\n')
# 	model = RandomForestClassifier(n_estimators=i, max_features=None)
# 	model.fit(X_train, y_train)

# 	y_pred = model.predict(X_test)
# 	accuracy = accuracy_score(y_test, y_pred)
# 	scores.append(accuracy)

# best_parameter = scores.index(max(scores)) + 1
param_grid = {
	'n_estimators': (10, 30, 50, 100, 200, 300, 400, 500, 700, 800, 1000),
	'max_features': ('auto', 'sqrt', 'log2', None),
	'criterion': ('gini', 'entropy')
}
gs = GridSearchCV(RandomForestClassifier(), param_grid, verbose=1, cv=5, n_jobs=-1)
model = gs.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(model.best_score_)
print(model.best_estimator_)
print(model.best_params_)
print('\n\n')
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))


# z_pred = best.predict([[63320, 4, 289]])
# print(z_pred)

filename = 'model_undersampled_1160.sav'
pickle.dump(model, open(filename, 'wb'))