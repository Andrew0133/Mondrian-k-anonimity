from classes.node import Node
from classes.data_frame_manager import DataFrameManager
import os

class Mondrian:
    def __init__(self, k: int, dfm: DataFrameManager, qi: list):
        self.k = k
        self.tree = Node(dfm.data)
        self.qi = qi

    def choose_dimension(self):
        """
        One heuristic, chooses the dimension with the widest (normalized) range of values.
        """
        qi_max = 0
        dim = None
        
        for q in self.qi:
            self.tree.sort_values(q)
            current_max = self.tree.data[q].iloc[-1] - self.tree.data[q].iloc[0]
            if current_max > qi_max:
                dim = q
                qi_max = current_max
        
        return dim

    def anonymize_aux(self):
        self.anonymize(self.tree)

    def anonymize(self, partition):
        if partition is None or len(partition.data.index) <= self.k:
            #no allowable multidimensional cut for partition            
            return
        else:
            dim = self.choose_dimension()
            fs = self.frequency_set(partition, dim)
            split_val = self.find_median(fs)
            partition.create_partition(dim, split_val, self.k)
          
            self.anonymize(partition.left)
            self.anonymize(partition.right)

    def frequency_set(self, partition, dim):    
        '''
        The frequency set of attribute A for partition P is the set of unique values of A in P, each paired with an integer 
        indicating the number of times it appears in P
        '''    
        return [value for value in partition.data[dim]]

    def find_median(self, fs):
        '''
        Standard median-finding algorithm
        '''
        return sum(fs) / len(fs)