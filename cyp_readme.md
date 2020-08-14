# 青岛啤酒（600600）股票分析

U201815324-气卓1801班-陈钰溥

## 一、简介

根据从网络上收集到的近一年青岛啤酒股票数据，我们组进行了有分工的数据分析。通过学习老师上课展示的课件以及网上有关数据分析的资料，我完成了大部分任务，编写了Python代码并进行了调试和分析，对金融数据分析有了进一步的认识。

## 二、利用数据得到k线

### 相关代码
```Python
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
```
### 解释与结果
1. 开头添加coding=gbk注释的原因是在代码调试过程中，总是出现“- coding: utf-8 -”错误，百度后添加注释使代码支持中文。
2. 导入matplotlib、pandas等库后，根据上课所学内容进行数据导入和清晰无用数据（但好像有时不需要），并将第一列设为index值，同时确保日期格式列保留。
```python
daily = pd.read_csv('600600kxian.csv',index_col=0,parse_dates=True)
```
3. 尝试利用函数输出line、renko、candle等形式的数据分析结果，下面是输出结果（数据范围:2019/7/1-2020/8/10）：
![zhexian_1](https://github.com/lahuan3369/MyPictures/blob/master/zhexian_1.png)
![zhexian_2](https://github.com/lahuan3369/MyPictures/blob/master/zhexian_2.png)
![zhexian_3](https://github.com/lahuan3369/MyPictures/blob/master/zhexian_3.png)
![zhexian_4](https://github.com/lahuan3369/MyPictures/blob/master/zhexian_4.png)

其中最后一张图结合了K线图、成交量柱状图和分别以3、6、9天为步长的曲线图，但由于数据过于密集，不利于观察与分析，后期需要进行改进。

## 三、MACD与EDA因子分析

相关代码
```python
# coding=gbk 
from datetime import datetime
import pylab as pl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

df = pd.read_csv('600600kxian.csv',index_col=0,parse_dates=True)

# 剔除缺失数据
df = df.dropna()
df.head()
# daily = daily.reset_index().drop(columns='index')
# daily.head()

df.index.name = 'Date'
df.shape
df.head(3)
df.tail(3)


# EMA指数移动平均线
num_periods_fast = 10  # 快速EMA的时间周期，10
# K:平滑常数，取2/(n+1)
K_fast = 2 / (num_periods_fast + 1)  # 快速EMA平滑常数
ema_fast = 0
num_periods_slow = 40  # 慢速EMA的时间周期，40
K_slow = 2 / (num_periods_slow + 1)  # 慢速EMA平滑常数
ema_slow = 0
num_periods_macd = 20  # MACD EMA的时间周期，20
K_macd = 2 / (num_periods_macd + 1)  # MACD EMA平滑常数
ema_macd = 0

ema_fast_values = []  
ema_slow_values = []  
macd_values = []  
macd_signal_values = []  
# MACD - MACD-EMA
MACD_hist_values = []  
for close_price in df['close']:
    if ema_fast == 0:  # 第一个值
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

# 设置画布，纵向排列的三个子图
fig, ax = plt.subplots(3, 1)

plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False

plt.subplots_adjust(hspace=.1)

ax[0].set_ylabel('Close price in ￥')
ax[0].set_title('青岛啤酒600600' )
close_price.plot(ax=ax[0], color='g', lw=1., legend=True, use_index=False)
ema_f.plot(ax=ax[0], color='b', lw=1., legend=True, use_index=False)
ema_s.plot(ax=ax[0], color='r', lw=1., legend=True, use_index=False)

ax[1] = plt.subplot(312, sharex=ax[0])
macd.plot(ax=ax[1], color='k', lw=1., legend=True, sharex=ax[0], use_index=False)
ema_macd.plot(ax=ax[1], color='g', lw=1., legend=True, use_index=False)

ax[2] = plt.subplot(313, sharex=ax[0])
df['MACD_hist'].plot(ax=ax[2], color='r', kind='bar', legend=True, sharex=ax[0])

# 设置合适的间隔，以便图形横坐标可以正常显示
interval = 5
# 设置x轴参数，应用间隔设置
# 时间序列转换
# x轴标签旋转便于显示
pl.xticks([i for i in range(1, 273 + 1, interval)],
          [datetime.strftime(i, format='%Y-%m-%d') for i in \
           pd.date_range(df.index[0], df.index[-1], freq='%dd' % (interval))],
          rotation=45)
plt.show()
```
### 解释与结果

由于时间和能力的限制，我只编写了macd因子代码的开头及结尾的部分内容，中间的主要的计算部分我通过在Github网站以及CSDN论坛中翻页查找，找到了较为简洁的计算代码。拷贝粘贴后，我又花了很长时间进行debug，不断排除错误，使得代码能够执行。

青岛啤酒（600600）2019/7/1-2020/3/27ClosePrice线、EMA快、慢线、MACD线如图：

![zhexian_5](https://github.com/lahuan3369/MyPictures/blob/master/zhexian_5.png)

## 总结

这次小组分工合作完成金融数据分析，我从中获益良多，对python编程有了进一步的认识。更大的收获在于更加熟练地利用Github及CSDN此类的专业平台，拓宽了视野和知识层次，对电脑技术的使用也更加熟练。