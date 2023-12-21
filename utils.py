import os
import argparse
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from datetime import datetime, timedelta

from tqdm import tqdm

from vnstock import stock_historical_data
#from sharpe_ratio_stats import estimated_sharpe_ratio, ann_estimated_sharpe_ratio, probabilistic_sharpe_ratio, num_independent_trials, expected_maximum_sr, deflated_sharpe_ratio

# one_day = timedelta(days=1)
# end = datetime.today()
# start = end - 730 * one_day

# start = start.strftime("%Y-%m-%d")
# end = end.strftime("%Y-%m-%d")

# print(f"start date: {start}")
# print(f"end date: {end}")

# tickers = ['HPG', 'HAX', 'MWG', 'GMD']

# benchmark = ["FUESSV50", "E1VFVN30",
#             "FUEVN100"]

def load_tickers(tickers, start, end):
    l = []
    # loop through tickers
    for i, tic in enumerate(tickers):
        print(f'Download ticker: {tic}')
        t = tic.lower()
        globals()[t] = stock_historical_data(tickers[i], 
                                   start,
                                   end, '1D')
        globals()[t]['return'] = globals()[t]['close'].pct_change()
        globals()[t]['time'] = pd.to_datetime(globals()[t]['time'], format="%Y-%m-%d")
        
        # print(f'{tic} na values: {globals()[t].isna().sum()}')
    # list of ticker dataframe
    l = [globals()[t.lower()] for t in tickers]
    return l

# ticker_list = load_tickers(tickers, start, end)
# ben_list = load_tickers(benchmark, start, end)

def combine_tickers(ticker_list, start, end):
    res = pd.DataFrame({'time':pd.date_range(start, end)})
    cols = ['time', 'close', 'return']
    
    for i in range(len(ticker_list)):
        ticker = ticker_list[i].ticker.iloc[0]
        temp = ticker_list[i][cols].rename(columns={'close':f'close_{ticker}',
                                                    'return':f'return_{ticker}'})\
                .drop_duplicates('time')

        res = res.merge(temp,
                        on='time',
                        how='left')

    return res

def combine_returns(asset_list):
    res = pd.DataFrame()

    for i in range(len(asset_list)):
        if  i == 0:
            asset = asset_list[0].ticker.iloc[0]   
            res = asset_list[0][['time', 'return']].rename(columns={'return':f'{asset}'})
        else:
            asset = asset_list[i].ticker.iloc[0]
            res = res.merge(asset_list[i][['time', 'return']],
                            on='time')\
                            .rename(columns={'return': f'{asset}'}) 
    res = res.rename(columns={'time': 'date'})
    res = res.set_index('date').dropna()
    return res 

# df = combine_returns(ticker_list) 


# ben = combine_returns(ben_list)

def generate_scenarios(M, etfs_returns):
 
    if os.getcwd()+'/models/' not in sys.path: 
        sys.path.append(os.getcwd()+'/models/')

    from TI import generate_random_weights, simulate 
    
    df_pfs_returns = pd.DataFrame()

    for i in tqdm(range(M)):
        _weights = generate_random_weights(etfs_returns)
        _pf_returns = simulate(etfs_returns, _weights)
        df_pfs_returns[i] = _pf_returns

    return df_pfs_returns

# df_pfs_returns = generate_scenarios(5000, ben)

# best_psr_pf_name = probabilistic_sharpe_ratio(returns=df_pfs_returns, sr_benchmark=0).sort_values(ascending=False).index[0]
# best_psr_pf_returns = df_pfs_returns[best_psr_pf_name]

# dsr = deflated_sharpe_ratio(trials_returns=df_pfs_returns, returns_selected=best_psr_pf_returns)
# dsr

def get_config(cliParams=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", action="store",required=True)

    if not cliParams:
        args = parser.parse_args()
    else:
        args = parser.parse_args(cliParams.split())
    return args.config

def main(cliParams=None):
    config_fname = get_config(cliParams)
    print(f"config file: {config_fname}")

'''
arguments: config file containing
    1. ticker_list
    2. ben_list for benchmarking
    3. start
    4. end
'''

def returns_to_equity(returns):
    equity = returns.add(1).cumprod().sub(1)
    return equity

def visualize(tickerDf, benDf, type):
    '''
    Visualize TIs
    :Params:
        tickerDf: portfolio dataframe
        benDf: benchmark dataframe
        type: which TI to visualize ?
    '''

def visualize_simulation(returns, top=5):
    top_psr_pf_name = probabilistic_sharpe_ratio(returns, sr_benchmark=0).sort_values(ascending=False).index[:top]
    returns[top_psr_pf_name].plot(figsize=(15,10), legend=True)

if __name__ == "__main__":
    main()
