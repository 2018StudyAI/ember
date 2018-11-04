# -*- coding:utf-8 -*-
import os
import argparse
import sys
from ember import PEFeatureExtractor
import tqdm
import jsonlines
import pandas as pd

path_label = ''

'''
    라벨값 가져오기
'''
def ExtractLabel(filename):
    data = pd.read_csv(path_label)
    filename = filename.split('/')[-1]
    return data[data.hash == filename].values[0][1]

def GetFileLists(path_datasets):
    filenames = []
    for filename in os.listdir(path_datasets):
        if os.path.isfile(os.path.join(path_datasets, filename)):
            _filename, extension = os.path.splitext(filename)
            #파일 확장자가 vir이면
            if extension == '.vir':
                filenames.append(filename)             

    return filenames

def ExtractFeatures(path_datasets, filesname, path_output):
    ErrorCount = 0
    extractor = PEFeatureExtractor()

    with jsonlines.open(os.path.join(path_output, "features.jsonl"), 'w') as f:
        for i in tqdm.tqdm(range(len(filesname))):
            _filename, extension = os.path.splitext(filesname[i])
            _file = os.path.join(path_datasets, filesname[i])
            binary = open(_file, 'rb').read()

            try:
                feature = extractor.raw_features(binary)
                feature.update({"sha256": _filename}) #hash
                feature.update({"label" : ExtractLabel(filesname[i])}) #label        
                f.write(feature)
            except KeyboardInterrupt:
                sys.exit()
            except:
                ErrorCount += 1

    print("Error : %d" % (ErrorCount))
                    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dirname", help="Directoryname including Datasets", required=True)
    parser.add_argument("-o", "--output", help="output Directory", required=True)
    parser.add_argument("-c", "--csv", help="filename including label", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.dirname):
        parser.error("ember model {} does not exist".format(args.dirname))
    if not os.path.exists(args.output):
        parser.error("ember model {} does not exist".format(args.output))
    if not os.path.exists(args.csv):
        parser.error("ember model {} does not exist".format(args.csv))

    path_datasets = args.dirname
    path_output = args.output
    global path_label
    path_label = args.csv

    filenames = GetFileLists(path_datasets)
    ExtractFeatures(path_datasets, filenames, path_output)
    
if __name__=='__main__':
    main()
    print("\n================ DONE ==================\n")