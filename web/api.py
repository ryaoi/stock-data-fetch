from os import path, mkdir
from datetime import datetime, date, timedelta
import pandas_datareader.data as web
import pandas as pd
import json
import requests

HOME_DIR = path.expanduser("~")


def M_to_digit(string):
    if 'M' in string:
        return string.replace(".", "").replace("M", "00000")
    return string


def get_rt_df_from_google(ticker):
    rsp = requests.get(('https://finance.google.com/finance?q=%s'
                        '&output=json') % (ticker))
    if rsp.status_code in (200,):
        fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
        data = {'Date': [date.today()],
                'Open': [float(fin_data['op'].replace(",", ""))] if fin_data['op'] is not None else float(-1),
                'High': [float(fin_data['hi'].replace(",", ""))] if fin_data['hi'] is not None else float(-1),
                'Low': [float(fin_data['lo'].replace(",", ""))] if fin_data['lo'] is not None else float(-1),
                'Close': [float(fin_data['l'].replace(",", ""))] if fin_data['l'] is not None else float(-1),
                'Adj Close': [float(fin_data['l'].replace(",", ""))] if fin_data['l'] is not None else float(-1),
                'Volume': [int(float(M_to_digit(fin_data['vo'].replace(",", ""))))] if fin_data['vo'] is not None else -1}
        df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        df.index = df['Date']
        del df['Date']
        print(df)
        return (df)
    else:
        print("Couldnt retrieve the live_prince from finance.google.com"
              "\nStatus Code:%d" % rsp.status_code)
        return None


def mkdir_if_not_exist(dir_path):
    if not path.exists(dir_path):
        mkdir(dir_path)


class DataReader(object):
    start = "1926-01-01"

    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir or path.join(HOME_DIR, "stock-data")
        mkdir_if_not_exist(self.cache_dir)

    def read(self, ticker, source="yahoo", end=None):
        if end is None:
            end = datetime.strftime(date.today(), '%Y-%m-%d')
        filename = path.join(self.cache_dir, ticker + ".csv")                         # filename = ticker.csv
        try:
            df = web.DataReader(ticker, source, start=self.start, end=end)            # Fetch the dataframe
        except Exception as e:
            print(("Can't retrieve the specified Data:ticker:"
                  "%s - source:%s" % (ticker, source)))
            print("[-]Error:" + str(e))
            return None                                                               # Return None
        if not path.isfile(filename):                                                 # If it's the first time fetching the data
            df.to_csv(filename, header=True)                                          # Save it to ticker.csv as a reference
            return df                                                                 # Return the dataframe that we saved
        else:

            filename_raw = path.join(self.cache_dir, ticker + "." + source + ".csv")  # Raw data name (ticker.source.csv)
            df.to_csv(filename_raw, header=True)                                      # Save raw data
            df_ref = pd.read_csv(filename, index_col=0)                               # Get the Reference data (ticker.csv)

            J = df_ref.iloc[-1]                                                       # Set J to the last date available inside the Reference data
            J = datetime.strptime(J.name, "%Y-%m-%d")                                 # str -> datetime
            end = datetime.strptime(end, "%Y-%m-%d")
            if end < J:                                                               # If end < J retrieve the data from reference data
                return df_ref.loc[self.start:datetime.strftime(end, '%Y-%m-%d')]
            else:                                                                     # Else renew the reference data
                start_date = df_ref.iloc[0].name
                end_date = (J-timedelta(days=1)).strftime("%Y-%m-%d")
                df_ret = df_ref.loc[start_date:end_date].reset_index()                # Retrieve the first dataframe for concatenating
                df_tmp = df.loc[J.strftime("%Y-%m-%d"):].reset_index()                # The Raw data to concatenate with the reference
                df_ret = df_ret.append(df_tmp, ignore_index=True)                     # Append the raw data to the reference
                df_rt_price = get_rt_df_from_google(ticker)                           # Get a Dataframe from finance.google.com
                if 'Adj Close' in df_ret.columns and 'Adj Close' in df:               # if "Adj Close" is in the Referenced dataframe and the raw
                    df.reset_index(inplace=True)
                    df_ret["Adj Close"] = df["Adj Close"]                             # Renew the reference data with Raw data
                elif 'Adj Close' not in df_ret:                                       # Otherwise delete the 'Adj Close' column of the new Dataframe
                    del df_rt_price['Adj Close']
                df_rt_price = df_rt_price.reset_index()
                if not df_rt_price.empty:                                             # if df from get_rt_live_price is not None
                    df_ret = df_ret.append(df_rt_price, ignore_index=True)            # Append our reference data with the df from get_rt_live_price
                df_ret['Date'] = pd.to_datetime(df_ret['Date'], format="%Y-%m-%d")    # Adjust the Time Format
                df_ret.index = df_ret['Date']                                         # Set Index to Date
                del df_ret['Date']                                                    # Delete "Date" Column from the dataframe
                df_ret.to_csv(filename, header=True)                                  # Save the new reference data
                return df_ret                                                         # Return the data


def data_reader(ticker, source="yahoo", end=None):
    try:
        return DataReader().read(ticker, source, end)                                 # Return Dataframe
    except Exception as e:                                                            # Handle Error in case it crash
        print("[-] Error: " + str(e))                                                 # Print the error message with more information
        return None                                                                   # Return None
