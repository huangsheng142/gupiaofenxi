# coding=gbk 
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

daily = pd.read_csv('600600kxian.csv',index_col=0,parse_dates=True)

# 剔除缺失数据
daily = daily.dropna()
daily.head()
# daily = daily.reset_index().drop(columns='index')
# daily.head()

daily.index.name = 'Date'
daily.shape
daily.head(3)
daily.tail(3)

import mplfinance as mpf
mpf.plot(daily)

mpf.plot(daily,type='line')
mpf.plot(daily, type='renko')
# mpf.plot(daily,type='ohlc',mav=4)
# # mpf.plot(daily,type='candle',mav=(3,6,9))
mpf.plot(daily,type='candle',mav=(3,6,9),volume=True)
plt.show()
