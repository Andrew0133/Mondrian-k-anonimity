from classes.data_frame_manager import DataFrameManager

def frequency_set(partition, dim):
    """
    The frequency set of attribute A for partition P is the set of unique values of A in P, each paired with an integer
    indicating the number of times it appears in P
    :param partition: Entire partition
    :param dim: Quasi identifier
    :return: Occurence number of quasi identifier
    """
    return [value for value in partition[dim]]

def find_median(fs):
    """
    Standard median-finding algorithm
    :param fs: Frequency set
    :return: Median value of fs
    """
    return sum(fs) / len(fs)

class Mondrian:
    def __init__(self, k: int, dfm: DataFrameManager, qi: list):
        self.k = k
        self.dfm = dfm
        self.qi = qi
        self.partitions = [ ] #used to store regions

    def choose_dimension(self, examined_qi):
        """
        One heuristic, chooses the dimension with the widest (normalized) range of values.
        :examined_qi: index of non-considered highest qi 
        :return: Quasi identifier
        """
        dim = { }

        for q in self.qi:
            self.sort_values(q)

            dim[q] = self.dfm.data[q].iloc[-1] - self.dfm.data[q].iloc[0]

        # sort dictionary using descending order
        dim = sorted(dim.items(), key=lambda x: x[1], reverse=True)
        return dim[examined_qi][0]

    def anonymize_aux(self):
        self.anonymize(self.dfm.data)
        self.generalize_region()

    def anonymize(self, partition, examined_qi=0):
        """
        A Greedy Partitioning Algorithm
        :param partition: Entire partition
        :examined_qi: Used to go the next qi in case of no allowable cut, based on normalization. Default 0, highest dimension
        :return: Anonymized data
        """
        # if the partition can't be splitted
        if len(partition) <= 2*self.k:
            self.partitions.append(partition)
            return

        # if qis are finished
        if examined_qi == len(self.qi):
            self.partitions.append(partition)
            return

        dim = self.choose_dimension(examined_qi)
        fs = frequency_set(partition, dim)
        split_val = find_median(fs)
        lhs_rhs = self.create_partition(partition, dim, split_val, self.k)

        if lhs_rhs:
            self.anonymize(lhs_rhs[0])
            self.anonymize(lhs_rhs[1])
        else: 
            examined_qi += 1
            self.anonymize(partition, examined_qi)

    def create_partition(self, partition, dim, split_val, k):
        """
        Partition function splits the current partition in two sub partitions based on a split_val parameter.
        :param partition: Entire partition
        :param dim: Quasi identifier
        :param split_val: Value used to split the partition
        :param k: Size of group
        :return: None if no allowable multidimensional cut for partition, sub partitions otherwise
        """
        partition_left = partition.loc[partition[dim] <= split_val]
        partition_right = partition.loc[partition[dim] > split_val]
        
        if len(partition_left) < k or len(partition_right) < k:
            return None

        return (partition_left, partition_right)

    def sort_values(self, qi):
        """
        Function used to sort data frame based on qi
        :param qi: Quasi identifier
        :return: Data Frame sorted
        """
        self.dfm.data.sort_values(by=qi, inplace=True)

    def generalize_region(self):
        """
        Recoding functions are constructed using summary statistics (Range statistic) from each region.
        :return: Generalized partition
        """
        generalized_partitions = []
        for partition in self.partitions:
            for q in self.qi:
                partition = partition.sort_values(by=q)
                min_val = partition[q].iloc[0]
                max_val = partition[q].iloc[-1]

                if q in self.dfm.decoding_dict:
                    generalized = ''

                    for row_value in partition[q].unique():
                        generalized += self.dfm.decoding_dict[q][row_value] + '~'
                    
                    generalized = generalized[:-1]
                    partition[q] = generalized
                else:
                    if min_val == max_val:
                        partition[q] = min_val
                    else:
                        partition[q] = f'{min_val}~{max_val}'

            generalized_partitions.append(partition)    

        self.partitions = generalized_partitions

    def write_on_file(self, path):
        self.dfm.write_output_file(self.partitions, path)

    def get_normalized_avg_equivalence_class_size(self):
        """
        get_normalized_avg_equivalence_class_size measures how well partitioning approaches the best case
        :return: avg
        """
        return (len(self.dfm.data) / len(self.partitions)) / self.k
            