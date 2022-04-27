import argparse
import pandas as pd
from config import DEBUG
from classes.data_frame_manager import DataFrameManager
from classes.mondrian import Mondrian
from datetime import datetime
import matplotlib.pyplot as plt

def plot_test(dfm, qi):
    print('Started ananomyzation testing for different k values - this operation can take several minutes')

    k_list = [ 2, 10, 20, 40, 60, 80, 100 ]

    avg_list = [ ]

    for k_value in k_list:
        if DEBUG:
            print('[DEBUG] - Started ananomyzation for k = %d' % k_value)

        mondrian = Mondrian(k_value, dfm, qi)
        mondrian.anonymize_aux()
        avg_list.append(round(mondrian.get_normalized_avg_equivalence_class_size(), 2))
        
        if DEBUG:
            print('[DEBUG] - Finished ananomyzation for k = %d' % k_value)

    fig, ax = plt.subplots(figsize=(12,8))
    plt.plot(k_list, avg_list, marker='o')
    plt.xlabel('k')
    plt.ylabel('Normalized average equivalence class size metric (C AVG)')
    plt.title('Normalized average equivalence class size metric (C AVG) vs k')

    for index in range(len(k_list)):
        ax.text(k_list[index], avg_list[index], avg_list[index])

    plt.xticks(k_list)
    plt.grid()
    plt.savefig('data/plot_output.jpg')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qi', help='Quasi Identifier', required=True, type=str, nargs='+')
    parser.add_argument('--k', help='K-Anonimity', required=True, type=int)
    parser.add_argument('--dataset', help='Dataset to be anonymized', required=True, type=str)
    parser.add_argument('--rid', help='Remove id column', type=str, choices=['y', 'n'])
    parser.add_argument('--plt', help='Test for different K saved in image', type=str, choices=['y', 'n'])

    args = parser.parse_args()

    k = args.k
    df = pd.read_csv(args.dataset)
    qi = args.qi

    if 'y' == args.rid:
       df.drop('id', inplace=True, axis=1) 

    if DEBUG:
        print('[DEBUG] - ORIGINAL DATASET')
        print(df)

    dfm = DataFrameManager(df, qi)

    mondrian = Mondrian(k, dfm, qi)

    print('Starting anonymization for k = %d' % k)
    start = datetime.now()
    mondrian.anonymize_aux()
    end = (datetime.now() - start).total_seconds()

    print('Finished in %.2f seconds (%.3f minutes (%.2f hours))' % (end, end / 60, end / 60 / 60))
    print('Normalized average equivalence class size metric AVG %.2f' % mondrian.get_normalized_avg_equivalence_class_size())
    
    print('Writing anonymized data on file')
    mondrian.write_on_file("data/output.csv")

    # used to test anonymization for different k values
    if 'y' == args.plt:
        plot_test(dfm, qi)
