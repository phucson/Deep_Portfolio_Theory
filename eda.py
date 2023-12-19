import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

from plotly import graph_objects as go

index_file = "VN30index.csv"
data_folder = './data/'

start_train = '2019-1-14'
end_train = '2021-1-1'

start_val = '2021-1-2'
end_val = '2023-12-17'

vn30 = ['ACB', 'BCM', 'BID', 'BVH', 'CTG',
        'FPT', 'GAS', 'GVR', 'HDB', 'HPG',
        'MBB', 'MSN', 'MWG', 'PLX', 'POW',
        'SAB', 'SHB', 'SSI', 'STB', 'TCB',
        'TPB', 'VCB', 'VHM', 'VIB', 'VIC',
        'VJC', 'VNM', 'VPB', 'VRE', 'SSB']

vn29 = ['ACB', 'BCM', 'BID', 'BVH', 'CTG',
        'FPT', 'GAS', 'GVR', 'HDB', 'HPG',
        'MBB', 'MSN', 'MWG', 'PLX', 'POW',
        'SAB', 'SHB', 'SSI', 'STB', 'TCB',
        'TPB', 'VCB', 'VHM', 'VIB', 'VIC',
        'VJC', 'VNM', 'VPB', 'VRE']

res = pd.DataFrame({'date': pd.date_range(start_train, end_val)})
date_range = res['date']
cols = ['date', 'close', 'return']

def data_prep(ticker_list, start, end):
    '''
    Read data and convert into usable format
    '''
    df_list = []

    for i, tic in enumerate(ticker_list):
        df = pd.read_csv(f"./data/{tic}.csv", index_col=None)[["Date", "Price", "Vol.", "Change %"]].rename(columns={"Date":"date",
                                                                                                            "Price":"close",
                                                                                                            "Vol.":"vol",
                                                                                                            "Change %":"pct"})
        start_d = pd.to_datetime(start, format="%Y-%m-%d")
        end_d = pd.to_datetime(end, format="%Y-%m-%d")

        df['date'] = pd.to_datetime(df['date'], format="%m/%d/%Y")
        df = df[(df.date >= start_d) & (df.date <= end_d)]
        df = df.drop_duplicates("date")
        df = df.sort_values(['date'], ascending=True)

        df['close'] = df['close'].str.replace(',', '').astype('float')

        df['vol'] = df['vol'].str.replace('M', '').str.replace('K', '')
        df['vol'] = df['vol'].astype('float').mul(1e6)

        df['pct'] = df['pct'].str.replace('%', '').astype('float').div(100)

        df_list.append(df)

    return df_list

def combine_price(tickers, stock_list, start, end):
    '''
    Combine all prices into a single file

    :Param stock_list: list of stocks (dataframe)
    :Param start: start date (string)
    :Param end: end date (string)

    :Return: A single dataframe with all prices
    '''
    date_range = pd.date_range(start, end)
    res = pd.DataFrame({"date":date_range})
    
    for i, tic in enumerate(tickers):
        res = res.merge(stock_list[i][['date', 'close']], on='date',
                        how='left') 
        res = res.rename(columns={'close':tic})
    
    res = res.dropna(thresh=2).ffill(axis=0)

    return res


stock_list = data_prep(vn29, start_train, end_val)
res = combine_price(vn29, stock_list, start_train, end_val)

for df in stock_list:
    print(df.shape)
    

per = res[['date']] 
net = res[['date']]

assert net.shape[0] == res.shape[0], "wrong net's shape"
assert per.shape[0] == res.shape[0], "wrong net's shape"

for i, tic in enumerate(vn29):
    net[tic] = res[tic].diff()
    per[tic] = res[tic].pct_change()

net.dropna(how='any', inplace=True)
per.dropna(how='any', inplace=True)

ind = pd.read_csv(data_folder+index_file, index_col=False)
ind = ind[['Date', 'Price', 'Change %']].rename(columns={'Price':'PX_LAST',
                                                         'Change %':'% Change' })
ind['Change'] = ind['PX_LAST'].diff()

ind = data_prep(['VN30index'], start_train, end_val)[0]

ind.drop(columns=['vol'], inplace=True)
ind.rename(columns={'date':'Date',
                    'close':'PX_LAST'},
                     inplace=True)
ind['Change'] = ind['PX_LAST'].diff()   
ind = ind.dropna(how='any')

start_train = net.date.iloc[0]
end_val = net.date.iloc[-1]

res = res[(res.date >= start_train) & (res.date <= end_val)]
res.tail()
res.head()

ind.head()
ind.tail()

ind.to_csv('vn30.csv', index=False)
res.to_csv('last_price.csv', index=False)
net.to_csv('net_change.csv', index=False)
per.to_csv('percentage_change.csv', index=False)
