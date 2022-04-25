import pandas as pd
from config import DEBUG
import os

def df_from_list(partitions):
    return pd.concat(partitions)

class DataFrameManager:
    def __init__(self, data, qis):
        self.encoding_dict = { }
        self.decoding_dict = { }
        self.data = data
        self.normalize_data(qis)

    def is_categorical_column(self, column):
        """
        Check if a column contains categorical values by looking the first row
        :param column: column
        :return: false if the first value is a number, true otherwise
        """
        try:
            if int(self.data[column][0]) == self.data[column][0]:
                return False
        except ValueError:
            return True

    def normalize_data(self, qis):
        """
        Normalize data function that transforms strings into numbers (for categorical data), skip column otherwise.
        """
        print('Starting normalization for categorical data - this operation can take several minutes')

        for qi in qis:
            uniques = self.data[qi].unique()

            if not self.is_categorical_column(qi):
                continue
                
            if qi not in self.encoding_dict:
                self.encoding_dict[qi] = { }
                self.decoding_dict[qi] = { }

            for unique in uniques:
                if unique not in self.encoding_dict[qi]:
                    if any(self.encoding_dict[qi]):
                        value = self.encoding_dict[qi][list(self.encoding_dict[qi].keys())[-1]] + 1
                    else:
                        value = 0

                    self.encoding_dict[qi][unique] = value
                    self.decoding_dict[qi][value] = unique

        self.data.replace(
            self.encoding_dict,
            inplace=True
        )
            
        if DEBUG:
            print('\n[DEBUG] - ENCODING AND DECODING DICTIONARIES')
            print(self.encoding_dict)
            print(self.decoding_dict)
        
        print('Finished normalization')

    def print_data(self):
        print(self.data)

    def write_output_file(self, partitions, path):
        """
        Function used to write generalized partitions on file
        :param partitions: List of sub partitions
        :param path: Path to save the file
        :return:
        """
        if not os.path.isfile(path):
            df_from_list(partitions).to_csv(path, header='column_names', index=False, sep=";")
        else:
            os.remove(path)
            df_from_list(partitions).to_csv(path, mode='a', header='column_names', index=False, sep=";")
