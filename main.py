import argparse
import pandas as pd

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
    
    def create_partition(self, dimension, split_val):
        left_data = []
        right_data = []

        for idx, row in self.data.iterrows():
            if (row[dimension] <= split_val):
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

    def anonymize(self):
        for dimension in self.qi:            
            partition = self.tree

            fs = self.frequency_set(partition, dimension)
            split_val = Mondrian.find_median(fs)
            print(split_val)
            self.tree.create_partition(dimension, split_val)
            self.tree.print_tree()
        
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

    mondrian = Mondrian(k, df, qi)
    mondrian.anonymize()