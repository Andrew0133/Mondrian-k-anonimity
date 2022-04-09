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

    def normalize_data(self, qis):
        """
        Normalize data function that transforms strings into numbers (for categorical data), skip column otherwise.
        """
        for index, row in self.data.iterrows():
            for qi in qis:
                if type(row[qi]) == int or type(row[qi]) == float:
                    continue
                
                if qi not in self.encoding_dict:
                    self.encoding_dict[qi] = { }
                    self.decoding_dict[qi] = { }

                if row[qi] not in self.encoding_dict[qi]:
                    if any(self.encoding_dict[qi]):
                        value = self.encoding_dict[qi][list(self.encoding_dict[qi].keys())[-1]] + 1
                    else:
                        value = 0

                    self.encoding_dict[qi][row[qi]] = value
                    self.decoding_dict[qi][value] = row[qi]

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

    def denormalize_data(self):
        """
        Function used to denormalize qi values.
        """
        for index, row in self.data.iterrows():
            for qi in self.decoding_dict.keys():
                self.data[qi].replace(
                    to_replace=[row[qi]],
                    value=self.decoding_dict[qi][row[qi]],
                    inplace=True
                )

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
