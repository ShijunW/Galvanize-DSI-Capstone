import pandas as pd


def read_file(filename):
    '''return Pandas DataFrame
    filename - path of the JSON file
    '''
    return pd.read_json(filename, lines=True)