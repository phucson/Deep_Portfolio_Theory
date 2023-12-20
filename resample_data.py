import pandas as pd

data_folder = './data/'
index_file = 'vn30.csv'

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


ind = pd.read_csv(data_folder+index_file, 
                  parse_dates=['Date'],
                  index_col='Date')
ind_w = ind.resample("W").mean().ffill()

last_price = pd.read_csv(data_folder+'last_price.csv', 
                  parse_dates=['date'],
                  index_col='date')
last_price_w = last_price.resample("W").mean().ffill()

net_change = pd.read_csv(data_folder+'net_change.csv', 
                  parse_dates=['date'],
                  index_col='date')
net_change_w = net_change.resample("W").mean().ffill()

pct_change = pd.read_csv(data_folder+'percentage_change.csv', 
                  parse_dates=['date'],
                  index_col='date')
pct_change_w = pct_change.resample("W").mean().ffill()

ind_w.to_csv(data_folder+'vn30w.csv')
last_price_w.to_csv(data_folder+'last_pricew.csv')
net_change_w.to_csv(data_folder+'net_changew.csv')
pct_change_w.to_csv(data_folder+'pct_changew.csv')
