#print accuarcy
from sklearn.metrics import confusion_matrix, accuracy_score
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--csv', required=True, help="result.csv")
args = parser.parse_args()

data = pd.read_csv(args.csv)

y = np.array(data.y)
y_pred = np.array(data.ypred)
maxacc = 0.0
threshold = 0.0

for x in np.arange(0.2, 0.95, 0.05):
	ypred = np.where(y_pred > x, 1, 0)
	acc = accuracy_score(y, ypred)

	if acc > maxacc:
		maxacc = acc
		threshold = x

y_pred = np.where(y_pred > threshold, 1, 0)
mt = confusion_matrix(y, y_pred)
print("thresdshold", threshold)
print('max accuracy : ', maxacc)
print(mt)
