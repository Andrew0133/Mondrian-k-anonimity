from classes.data_frame_manager import DataFrameManager

from config import DEBUG

class Mondrian:
    def __init__(self, k: int, dfm: DataFrameManager, qi: list):
        self.k = k
        self.dfm = dfm
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
            current_max = self.dfm.data[q].iloc[-1] - self.dfm.data[q].iloc[0]
            if current_max > qi_max:
                dim = q
                qi_max = current_max
        
        return dim

    def anonymize_aux(self):
        self.anonymize(self.dfm.data)

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
            if DEBUG:
                print(partition)
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
        self.dfm.data.sort_values(by=qi, inplace=True)

    def generalize_region(self):
        generalized_partitions = []
        for partition in self.partitions:
            for q in self.qi:
                partition = partition.sort_values(by=q)
                min_val = partition[q].iloc[0]
                max_val =  partition[q].iloc[-1]

                if min_val == max_val:
                    partition[q] = min_val
                else:
                    if q in self.dfm.decoding_dict:
                        generalized = ''
                        for row_value in partition[q].unique():
                            generalized += self.dfm.decoding_dict[q][row_value] + '~'
                        generalized = generalized[:-1]
                        partition[q] = generalized
                    else:
                        partition[q] = f'{min_val}~{max_val}'

            generalized_partitions.append(partition)    

        self.partitions = generalized_partitions

    def write_on_file(self, path):
        self.dfm.write_output_file(self.partitions, path)
            