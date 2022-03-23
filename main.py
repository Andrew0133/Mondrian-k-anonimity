import argparse
import pandas as pd
from config import DEBUG

class DataFrameManager():
    def __init__(self, data, qis):
        self.encoding_dict = { }
        self.decoding_dict = { }
        self.data = data
        self.normalize_data(qis)

    def normalize_data(self, qis):
        """
        used to normalize data

        transforms strings into numbers
        """

        for index, row in df.iterrows():
            for qi in qis:
                #skip row if the type is already a number
                if type(row[qi]) == int or type(row[qi]) == float:
                    continue
                
                #if the qi is not in dicts add it
                if qi not in self.encoding_dict:
                    self.encoding_dict[qi] = { }
                    self.decoding_dict[qi] = { }

                #if the value of the qi is not in dicts add it
                if row[qi] not in self.encoding_dict[qi]:
                    if any(self.encoding_dict[qi]):
                        value = self.encoding_dict[qi][list(self.encoding_dict[qi].keys())[-1]] + 1
                    else:
                        value = 0

                    self.encoding_dict[qi][row[qi]] = value
                    self.decoding_dict[qi][value] = row[qi]

                #replace value in dataframe with a number value
                self.data[qi].replace(
                    to_replace=[row[qi]],
                    value=self.encoding_dict[qi][row[qi]],
                    inplace=True
                )

        if DEBUG:
            print('\nENCODING AND DECODING DICTIONARIES')
            print(self.encoding_dict)
            print(self.decoding_dict)

    def print_data(self):
        print(self.data)

    def write_data_on_file(self):
        pass

    def denormalize_data(self):
        """
        used to denormalize qi values
        """
        
        for index, row in df.iterrows():
            for qi in self.decoding_dict.keys():
                df[qi].replace(
                    to_replace=[row[qi]],
                    value=self.decoding_dict[qi][row[qi]],
                    inplace=True
                )

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert_left(self, data):
        if self.left is None:
            self.left = Node(data) 
        else:
            self.left.insert_left(data)

    def insert_right(self, data):
        if self.right is None:
            self.right = Node(data) 
        else:
            self.right.insert_left(data)

    def print_tree(self):
        if self.left:
            self.left.print_tree()
        
        print(self.data)
        
        if self.right:
            self.right.print_tree()
    
    def create_partition(self, dimension, split_val, k):
        left_data = []
        right_data = []

        for idx, row in self.data.iterrows():
            if row[dimension] <= split_val and len(pd.unique(self.data[dimension])) > k:
                left_data.append(row)
            elif row[dimension] < split_val:
                left_data.append(row)
            else:
                right_data.append(row)

        if left_data:
            self.left = Node(pd.DataFrame(left_data, columns=self.data.columns))
    
        if right_data:
            self.right = Node(pd.DataFrame(right_data,columns=self.data.columns))

class Mondrian:
    def __init__(self, k: int, df: pd.DataFrame, qi: list):
        self.k = k
        self.tree = Node(df)
        self.qi = qi

    def anonymize_aux(self):
        self.anonymize(self.tree, qi_index=0)

    def anonymize(self, partition, qi_index):
        if qi_index >= len(self.qi):
            qi_index = 0 #restart to split

        if len(partition.data.index) <= k:
            return
        else:
            fs = self.frequency_set(partition, self.qi[qi_index])
            split_val = Mondrian.find_median(fs)
            partition.create_partition(self.qi[qi_index], split_val, self.k)
            partition.print_tree()
            qi_index += 1
            
            self.anonymize(partition.left, qi_index)
            self.anonymize(partition.right, qi_index)
            
        
    def frequency_set(self, partition, dimension):
        frequency = {}
        
        for value in partition.data[dimension]:
            if value in frequency:
                frequency[value] += 1
            else:
                frequency[value] = 1    

        return frequency

    @staticmethod
    def find_median(fs):
        return max(fs, key=fs.get)
        
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
    
    if DEBUG:
        print('\nNORMALIZED DATA')
        dfm.print_data()
        dfm.denormalize_data()

        print('\nDENORMALIZED DATA')
        dfm.print_data()

    #mondrian = Mondrian(k, df, qi)
    #mondrian.anonymize_aux()