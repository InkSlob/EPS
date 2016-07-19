import urllib2
import datetime
from StringIO import StringIO
import numpy as np
import pandas as pd
import math

#estimates for calculation
YrEPS = 0.08 #EPS annual growth rate (8-12%)
YrPE = 0.08 #P/E annual growth rate (8-12%)
ROI = 0.15 #expected return on investment 15%

data = pd.read_csv('05092105SAT_APIdata.csv') #, index_col=0

data.columns=(['prev_close', 'dividend', 'EPS', 'PE', 'NA1', 'NA2', 'Change', 'Symbol', 'Volume'])

data['div5'] = data['dividend'] * 5
data['yr_EPS_earn_5'] = data['EPS']*math.pow(1+YrEPS,5)
data['yr_Proj_Stock_5'] = YrPE*data['yr_EPS_earn_5']*100
data['five_yr_stock_div'] = data['div5'] + data['yr_Proj_Stock_5']
data['fair_price'] = data['five_yr_stock_div']/(math.pow(1+ROI,5))
data['VALUE'] = data['fair_price'] - data['prev_close']

np.sort(data, axis=0)
print data[['VALUE','Symbol']]
