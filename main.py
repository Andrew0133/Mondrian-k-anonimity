import argparse
import pandas as pd
from config import DEBUG
from classes.data_frame_manager import DataFrameManager
from classes.mondrian import Mondrian
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qi', help='Quasi Identifier', required=True, type=str, nargs='+')
    parser.add_argument('--k', help='K-Anonimity', required=True, type=int)
    parser.add_argument('--dataset', help='Dataset to be anonymized', required=True, type=str)
    parser.add_argument('--rid', help='Remove id column', type=str, choices=['y', 'n'])
    args = parser.parse_args()

    k = args.k
    df = pd.read_csv(args.dataset)
    qi = [x for x in args.qi]

    if 'y' == args.rid:
       df.drop('id', inplace=True, axis=1) 

    if DEBUG:
        print('ORIGINAL DATASET')
        print(df)

    dfm = DataFrameManager(df, qi)

    mondrian = Mondrian(k, dfm, qi)
    mondrian.anonymize_aux()
    mondrian.generalize_region()
    mondrian.write_on_file("data/output.csv")
