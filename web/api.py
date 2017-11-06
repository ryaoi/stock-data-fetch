from os import path, mkdir
from datetime import datetime
import pandas_datareader.data as web

HOME_DIR = path.expanduser("~")


def mkdir_if_not_exist(dir_path):
    if not path.exists(dir_path):
        mkdir(dir_path)


class DataReader(object):
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir or path.join(HOME_DIR, "stock-data")
        mkdir_if_not_exist(self.cache_dir)

    def read(self, ticker, source, start="1990-01-01", end=None):
        end = end or datetime.now().date()
        filename = path.join(self.cache_dir, ticker + ".csv")
        df = web.DataReader(ticker, source, start, end)
        df.to_csv(filename, header=True)
        return df


def data_reader(ticker, source, start="1990-01-01", end=None):
    return DataReader().read(ticker, source, start, end)
