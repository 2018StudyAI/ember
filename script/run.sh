python ../01_extract.py -d ~/Downloads/traintest -c ~/Downloads/TrainSet.csv -o ~/Downloads/changedembertest
python ../02_train.py -d ~/Downloads/changedembertest
python ../03_predict.py -m ~/Downloads/changedembertest  -d ~/Downloads/traintest -c ~/Downloads/TrainSet.csv -o ~/Downloads/changedembertest
python ../04_get_accuarcy.py -c ~/Downloads/changedembertest/predict_with_label.csv -o ~/Downloads

