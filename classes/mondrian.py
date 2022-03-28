from classes.data_frame_manager import DataFrameManager
import os

class Mondrian:
    def __init__(self, k: int, dfm: DataFrameManager, qi: list):
        self.k = k
        self.data = dfm.data
        self.qi = qi
        self.partitions = [ ] #used to store regions

    def choose_dimension(self):
        """
        One heuristic, chooses the dimension with the widest (normalized) range of values.
        """
        qi_max = 0
        dim = None
        
        for q in self.qi:
            self.sort_values(q)
            current_max = self.data[q].iloc[-1] - self.data[q].iloc[0]
            if current_max > qi_max:
                dim = q
                qi_max = current_max
        
        return dim

    def anonymize_aux(self):
        self.anonymize(self.data)

    def anonymize(self, partition):
        if partition is None or len(partition.index) <= self.k:            
            return #no allowable multidimensional cut for partition
        else:
            dim = self.choose_dimension()
            fs = self.frequency_set(partition, dim)
            split_val = self.find_median(fs)
            lhs_rhs = self.create_partition(partition, dim, split_val, self.k)

        if lhs_rhs:
            self.anonymize(lhs_rhs[0])
            self.anonymize(lhs_rhs[1])
        else: #append partition to result
            self.partitions.append(partition)

    def create_partition(self, partition, dim, split_val, k):
        """
        Partition function
        """
        partition_left = partition.loc[partition[dim] <= split_val]
        partition_right = partition.loc[partition[dim] > split_val]
        
        if len(partition_left) < k or len(partition_right) < k:
            return None
        
        return (partition_left, partition_right)

    def frequency_set(self, partition, dim):    
        '''
        The frequency set of attribute A for partition P is the set of unique values of A in P, each paired with an integer 
        indicating the number of times it appears in P
        '''    
        return [value for value in partition[dim]]

    def find_median(self, fs):
        '''
        Standard median-finding algorithm
        '''
        return sum(fs) / len(fs)

    def sort_values(self, qi):
        self.data.sort_values(by=qi, inplace=True)