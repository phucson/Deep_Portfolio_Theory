import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

from plotly import graph_objects as go

stock_file = "VN30.xlsx"
index_file = "VN30index.csv"

stocks = pd.read_excel(stock_file, sheet_name=None,
                      index_col=None, na_values='NA',
                      usecols=["Ngày", "Lần cuối", "KL", "% Thay đổi"])

for i, st in enumerate(stocks.keys()):
    stocks[st] = stocks[st].rename(columns={"Ngày":"date",
                            "Lần cuối":"close",
                            "KL":"vol",
                            "% Thay đổi":"pct"})
    stocks[st]['date'] = pd.to_datetime(stocks[st]['date'], format="%d/%m/%Y")

