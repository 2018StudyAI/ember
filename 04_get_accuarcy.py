from sklearn.metrics import confusion_matrix, accuracy_score
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--csv', type=str, required=True, help='csv file for getting accuracy')
args = parser.parse_args()

def main():
    data = pd.read_csv(args.csv)

    y = data.y
    ypred = np.where(np.array(data.ypred) > 0.75, 1, 0)
    accuracy = accuracy_score(y, ypred)
    print("accuracy : %.2f%%" % (np.round(accuracy, decimals=2)*100))

if __name__=='__main__':
    main()