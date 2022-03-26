import argparse
import pandas as pd
from config import DEBUG
from classes.data_frame_manager import DataFrameManager
from classes.mondrian import Mondrian
from classes.output_file_manager import OutputFileManager
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qi', help='Quasi Identifier', required=True, type=str, nargs='+')
    parser.add_argument('--k', help='K-Anonimity', required=True, type=int)
    parser.add_argument('--dataset', help='Dataset to be anonymized', required=True, type=str)
    parser.add_argument('--dgh', help='Domain Generalization Hierarchy', required=True, type=str)
    args = parser.parse_args()

    k = args.k
    df = pd.read_csv(args.dataset)
    qi = [x for x in args.qi]

    if DEBUG:
        print('ORIGINAL DATASET')
        print(df)

    dfm = DataFrameManager(df, qi)

    mondrian = Mondrian(k, dfm, qi)
    mondrian.anonymize_aux()

    if DEBUG:
        print('file result')
        mondrian.tree.print_leaf()

    dataframe_output = mondrian.tree.concat_leaf()

    #ofm = OutputFileManager('data/output.csv', dataframe_output)
    #ofm.write_output_file()
    
    if DEBUG:
        print('\nNORMALIZED DATA')
        dfm.print_data()
        dfm.denormalize_data()

        print('\nDENORMALIZED DATA')
        dfm.print_data()