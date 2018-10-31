#!/usr/bin/env python
import os
import ember
import argparse
import lightgbm as lgb
import argparse
import tqdm
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, roc_curve, auc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--modelpath", type=str, required=True, help="trained model path")
    parser.add_argument("-d", "--datadir", type=str, help="Directory for predicting dataSets", required=True)
    parser.add_argument("-c", "--csv", type=str, help="Answer file", required=True)
    parser.add_argument("-o", "--output", type=str, help="output label and y_pred", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.modelpath):
        parser.error("ember model {} does not exist".format(args.modelpath))

    model_path = os.path.join(args.modelpath, "model.txt")
    lgbm_model = lgb.Booster(model_file=model_path)

    #read answer sheet
    data = pd.read_csv(args.csv)

    errorcount = 0
    y_pred = []
    y = []
    _name = []

    for filename in tqdm.tqdm(os.listdir(args.datadir)):
        _file = os.path.join(args.datadir, filename)

        if os.path.isfile(_file):
            binary = open(_file, "rb").read()

            try:
                y_pred.append(ember.predict_sample(lgbm_model, binary))
                y.append(data[data.hash == filename].values[0][1])
                _name.append(filename)
            except KeyboardInterrupt:
                sys.exit()
            except:
                errorcount += 1

    #print accuracy
    y_pred_01 = np.array(y_pred)
    y_pred_01 = np.where(y_pred_01 > 0.75, 1, 0)   
    acc_lgbm = accuracy_score(y, y_pred_01)
    print("accuaracy : ", acc_lgbm)

    mt = confusion_matrix(y, y_pred_01)
    print(mt)
    print("Error : %d" % (errorcount))

    #save csv
    r = pd.DataFrame({'hash': _name, 'label': y, 'y_pred': y_pred})
    r.to_csv(os.path.join(args.modelpath, args.output))


if __name__ == "__main__":
    main()