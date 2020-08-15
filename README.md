# 股票分析团队作业
### 团队成员：
#### 黄闽杰（组长）   U201812061
#### 蒋雨潇           U201811847
#### 陈钰溥           U201815324
# 所涉及到的库
tushare、pandas、numpy、seaborn、pylab、matplotlib、mplfinance
# 代码主要功能
#### 1.获取青岛啤酒股票（600600)2019年7月1日到2020年8月10日之间k线数据
#### 2.计算各变量相关系数矩阵
#### 3.绘制收盘价格与交易量关系散点图
#### 4.绘制开盘价格折线图
#### 5.计算EMA、MACD，并绘制EMA、MACD、K线
#### 6.计算RSI，绘制RSI、成交量图
# 探索性分析结论
#### 1. 分析青岛啤酒年K线，总体呈现平稳上升的态势，且目前并未到达历史高位，考虑到实际现实中的疫情影响导致消费水平、消费能力的下降，青岛啤酒的股价或处于平台期，波动不大，适合观望或持股待出。
#### 2. 当前青岛啤酒计算离差值（DIF）和慢速线（DEA）均大于0，即在图形上表示为它们处于零线以上，并向上移动，表示青岛啤酒股价行情处于多头行情中，可以买入开仓或多头持仓。
#### 3. 青岛啤酒MACD柱为金叉状态，表示应买入，市场由空头转为多头
