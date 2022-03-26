from operator import index
import os

class OutputFileManager:
    def __init__(self, path, df):
        self.path = path
        self.df = df

    def write_output_file(self):
        if not os.path.isfile(self.path):
            self.df.to_csv(self.path, header='column_names', index=False)
        else:
            os.remove(self.path)
            self.df.to_csv(self.path, mode='a', header=False, index=False)