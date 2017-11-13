from os import path
from shutil import rmtree
from unittest import TestCase
import mock
import pandas as pd
import pandas.util.testing as pdt

from .. import api

TEST_DIR = path.dirname(__file__)


def _read_time_series_csv(filename):
    return pd.read_csv(filename, parse_dates=True, index_col=0)


def web_reader(ticker, *args, **kwargs):
    filename = path.join(TEST_DIR, "mock-stock-data", ticker + ".csv")
    return _read_time_series_csv(filename)


@mock.patch(api.__name__ + ".mkdir")
def test_mkdir_if_not_exist(m_mkdir):
    dir_path = path.join(TEST_DIR, "dummy")
    api.mkdir_if_not_exist(dir_path)
    m_mkdir.assert_called_with(dir_path)


class DataReaderTest(TestCase):
    stock_data_dir = path.join(TEST_DIR, "stock-data")

    def setUp(self):
        api.HOME_DIR = TEST_DIR
        patcher1 = mock.patch(api.__name__ + ".web.DataReader",
                              side_effect=web_reader)
        self.m_web_reader = patcher1.start()
        self.addCleanup(patcher1.stop)
        self.reader = api.DataReader()

    def test_cache_dir(self):
        self.assertEqual(self.reader.cache_dir, self.stock_data_dir)

    def test_data_reader(self):
        ticker = "GOOG"
        end = "2017-11-03"
        df = api.data_reader(ticker, end=end)
        self.m_web_reader.assert_called_with(
            ticker, "yahoo", start="1926-01-01", end=end
        )
        expected = web_reader(ticker)
        pdt.assert_frame_equal(df, expected)

    def test_different_type_of_source(self):
        """
        From pandas-datareader Documentation
        Supported Sources with `pandas_datareader.data_reader` are:
        - Yahoo! Finance                   [Yes]
        - Google Finance                   [Yes]
        - Enigma                           [Nope]
        - Quandl                           [Yes]
        - St.Louis FED(RFED)               [Yes]
        - Kenneth French's data library    [Yes]
        - World Bank                       [No]
        - OECD                             [Yes]
        - Eurostat                         [Yes]
        - Thrifts Saving plan              [No]
        - Nasdaq Trader symbol definitions [No]
        """
        df = api.data_reader("F", "yahoo")                # Can Retrieve
        df = api.data_reader("F", "google")               # Can Retrieve
        df = api.data_reader("WIKI/AAPL", "quandl")
        df = api.data_reader("GDP", "fred")               # Can Retrieve
        df = api.data_reader("5_Industry_Portfolios", "famafrench") # data_reader doesn't return a dataframe, it returns a dict
        df = api.data_reader('UN_DEN', 'oecd')             # Can't retrieve 
        df = api.data_reader("tran_sf_railac", 'eurostat') # Can't retrieve

    def test_ticker_goog_different_source(self):
        df = api.data_reader("GOOG", "yahoo")              # OK
        df = api.data_reader("GOOG", "google")             # OK
        df = api.data_reader("GOOG", "quandl")             # OK (not updated)
        df = api.data_reader("GOOG", "fred")               # No
        df = api.data_reader("GOOG", "famafrench")         # No
        df = api.data_reader("GOOG", 'oecd')               # No
        df = api.data_reader('GOOG', 'eurostat')           # No

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.stock_data_dir)
