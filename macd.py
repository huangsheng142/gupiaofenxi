# coding=gbk 
from datetime import datetime
import pylab as pl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

df = pd.read_csv('600600kxian.csv',index_col=0,parse_dates=True)

# �޳�ȱʧ����
df = df.dropna()
df.head()
# daily = daily.reset_index().drop(columns='index')
# daily.head()

df.index.name = 'Date'
df.shape
df.head(3)
df.tail(3)


# EMAָ���ƶ�ƽ����
num_periods_fast = 10  # ����EMA��ʱ�����ڣ�10
# K:ƽ��������ȡ2/(n+1)
K_fast = 2 / (num_periods_fast + 1)  # ����EMAƽ������
ema_fast = 0
num_periods_slow = 40  # ����EMA��ʱ�����ڣ�40
K_slow = 2 / (num_periods_slow + 1)  # ����EMAƽ������
ema_slow = 0
num_periods_macd = 20  # MACD EMA��ʱ�����ڣ�20
K_macd = 2 / (num_periods_macd + 1)  # MACD EMAƽ������
ema_macd = 0

ema_fast_values = []  
ema_slow_values = []  
macd_values = []  
macd_signal_values = []  
# MACD - MACD-EMA
MACD_hist_values = []  
for close_price in df['close']:
    if ema_fast == 0:  # ��һ��ֵ
        ema_fast = close_price
        ema_slow = close_price
    else:
        ema_fast = (close_price - ema_fast) * K_fast + ema_fast
        ema_slow = (close_price - ema_slow) * K_slow + ema_slow

    ema_fast_values.append(ema_fast)
    ema_slow_values.append(ema_slow)

	# MACD is fast_MA - slow_EMA
    macd = ema_fast - ema_slow  
    if ema_macd == 0:
        ema_macd = macd
    else:
    	# signal is EMA of MACD values
        ema_macd = (macd - ema_macd) * K_macd + ema_macd  
    macd_values.append(macd)
    macd_signal_values.append(ema_macd)
    MACD_hist_values.append(macd - ema_macd)

df = df.assign(ClosePrice=pd.Series(df['close'], index=df.index))
df = df.assign(FastEMA10d=pd.Series(ema_fast_values, index=df.index))
df = df.assign(SlowEMA40d=pd.Series(ema_slow_values, index=df.index))
df = df.assign(MACD=pd.Series(macd_values, index=df.index))
df = df.assign(EMA_MACD20d=pd.Series(macd_signal_values, index=df.index))
df = df.assign(MACD_hist=pd.Series(MACD_hist_values, index=df.index))

close_price = df['ClosePrice']
ema_f = df['FastEMA10d']
ema_s = df['SlowEMA40d']
macd = df['MACD']
ema_macd = df['EMA_MACD20d']
macd_hist = df['MACD_hist']

# ���û������������е�������ͼ
fig, ax = plt.subplots(3, 1)

plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False

plt.subplots_adjust(hspace=.1)

ax[0].set_ylabel('Close price in ��')
ax[0].set_title('�ൺơ��600600' )
close_price.plot(ax=ax[0], color='g', lw=1., legend=True, use_index=False)
ema_f.plot(ax=ax[0], color='b', lw=1., legend=True, use_index=False)
ema_s.plot(ax=ax[0], color='r', lw=1., legend=True, use_index=False)

ax[1] = plt.subplot(312, sharex=ax[0])
macd.plot(ax=ax[1], color='k', lw=1., legend=True, sharex=ax[0], use_index=False)
ema_macd.plot(ax=ax[1], color='g', lw=1., legend=True, use_index=False)

ax[2] = plt.subplot(313, sharex=ax[0])
df['MACD_hist'].plot(ax=ax[2], color='r', kind='bar', legend=True, sharex=ax[0])

# ���ú��ʵļ�����Ա�ͼ�κ��������������ʾ
interval = 5
# ����x�������Ӧ�ü������
# ʱ������ת��
# x���ǩ��ת������ʾ
pl.xticks([i for i in range(1, 273 + 1, interval)],
          [datetime.strftime(i, format='%Y-%m-%d') for i in \
           pd.date_range(df.index[0], df.index[-1], freq='%dd' % (interval))],
          rotation=45)
plt.show()
