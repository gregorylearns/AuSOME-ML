import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

file = pd.read_csv('Hsc40_Area_NofPeaks_Length_Height_reduced.csv')

filename = []
label = []
area = []
no_of_peaks = []
length = []
height = []

for i in range(len(file)):
	filename.append(file.iat[i, 0])
	label.append(file.iat[i, 1])
	area.append(file.iat[i, 2])
	no_of_peaks.append(file.iat[i, 3])
	length.append(file.iat[i, 4])
	height.append(file.iat[i, 5])

matrix = [filename, area, no_of_peaks, length, height]
with_filename = np.column_stack(matrix)
y = label
# one = 0
# zero = 0
# for i in range(len(y)-1):
# 	if y[i] == 1:
# 		one += 1
# 	elif y[i] == 0:
# 		zero += 1
# print(f'Ones: {one}		Zeroes: {zero}')

# sm = SMOTE()
# X_res, y_res = sm.fit_resample(X, y)

# print(y_res)
# one = 0
# zero = 0
# for i in range(len(y_res)-1):
# 	if y_res[i] == 1:
# 		one += 1
# 	elif y_res[i] == 0:
# 		zero += 1
# print(f'Ones: {one}		Zeroes: {zero}')

X_train, X_test, y_train, y_test = train_test_split(with_filename, y, test_size=0.25)

test_matrix = [X_test, y_test]
test_data = np.column_stack(test_matrix)
pd.DataFrame(test_data).to_csv("test_data.csv", index=False)

X_test = X_test[:, 1:]
X_train = X_train[:, 1:]
# ss = StandardScaler()
# X_train = ss.fit_transform(X_train)
# X_test = ss.transform(X_test)

# scores = []

# for i in range(1, 1000):
# 	print(f'Getting accuracy score for n_estimators = {i}...\n')
# 	model = RandomForestClassifier(n_estimators=i, max_features=None)
# 	model.fit(X_train, y_train)

# 	y_pred = model.predict(X_test)
# 	accuracy = accuracy_score(y_test, y_pred)
# 	scores.append(accuracy)

# best_parameter = scores.index(max(scores)) + 1
param_RandomForest = {
	'n_estimators': (10, 30, 50, 100, 200, 300, 400, 500, 700, 800, 1000),
	'max_features': ('auto', 'sqrt', 'log2', None),
	'criterion': ('gini', 'entropy')
}
param_KNeighbors = {
	'n_neighbors': (3, 5, 7, 9, 11, 13, 15),
	'weights': ('uniform', 'distance'),
	'algorithm': ('ball_tree', 'kd_tree', 'brute', 'auto')
}
gs_RandomForest = GridSearchCV(RandomForestClassifier(), param_RandomForest, verbose=1, cv=5, n_jobs=-1)
model1 = gs_RandomForest.fit(X_train, y_train)
y_pred = model1.predict(X_test)

gs_KNeighbors = GridSearchCV(KNeighborsClassifier(), param_KNeighbors, verbose=1, cv=5, n_jobs=-1)
model2 = gs_KNeighbors.fit(X_train, y_train)
z_pred = model2.predict(X_test)

print('\nFor Random Forest:\n')
print(model1.best_score_)
print(model1.best_estimator_)
print(model1.best_params_)
print('\n\n')
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

print('\nFor KNeighbors:\n')
print(model2.best_score_)
print(model2.best_estimator_)
print(model2.best_params_)
print('\n\n')
print(confusion_matrix(y_test, z_pred))
print(classification_report(y_test, z_pred))
print(accuracy_score(y_test, z_pred))
# z_pred = best.predict([[63320, 4, 289]])
# print(z_pred)

filename1 = 'Hsc40_model_RandomForest.sav'
filename2 = 'Hsc40_model_KNeighbors.sav'
pickle.dump(model1, open(filename1, 'wb'))
pickle.dump(model2, open(filename2, 'wb'))