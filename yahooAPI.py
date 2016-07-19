import urllib2
import datetime
from StringIO import StringIO
import numpy as np
import pandas as pd
import math

stamp = '05092105SAT'
filename = stamp + '_APIdata.csv'
f = open(filename, 'a')

sfile = 'nasdaq.txt'

with open(sfile) as fS:
    content = fS.readlines()

f_size = len(content)
x = 100
count = 0 
scnt = 0
outer = f_size / 100
outer = int(outer)
print "THE STOCKS ARE: ", f_size
for i in range(outer):
    ustck = ''
    S = ''
    for k in range(x):
        if count < f_size:
            S = content[scnt]
            S = S.rstrip()
            if k < 1:
                ustck = S 
            else:
                ustck = ustck + ',' + S
            url1 = 'http://download.finance.yahoo.com/d/quotes.csv?s='
            url2 = '&f=pder=.csv' 
            url = url1 + ustck + url2
            scnt = scnt + 1
        else:
            break
    count = count + 1
    print url
    response = urllib2.urlopen(url)
    data = response.read()
    f.write(data)
f.close()
print "API CSV Obtained."

#estimates for calculation
YrEPS = 0.08 #EPS annual growth rate (8-12%)
YrPE = 0.08 #P/E annual growth rate (8-12%)
ROI = 0.15 #expected return on investment 15%

data = pd.read_csv(filename) #, index_col=0

data.columns=(['prev_close', 'dividend', 'EPS', 'PE', 'NA1', 'NA2', 'Change', 'Symbol', 'Volume'])

data['div5'] = data['dividend'] * 5
data['yr_EPS_earn_5'] = data['EPS']*math.pow(1+YrEPS,5)
data['yr_Proj_Stock_5'] = YrPE*data['yr_EPS_earn_5']*100
data['five_yr_stock_div'] = data['div5'] + data['yr_Proj_Stock_5']
data['fair_price'] = data['five_yr_stock_div']/(math.pow(1+ROI,5))
data['VALUE'] = data['fair_price'] - data['prev_close']



#fout = open('valueoutput.txt', 'w')
#fout.write()
#fout.close()

data = data[data.VALUE >= 0]
data = data.sort(['VALUE'])

print data[['Symbol', 'dividend', 'EPS', 'fair_price', 'prev_close', 'VALUE']]
data[['Symbol', 'dividend', 'EPS', 'fair_price', 'prev_close', 'VALUE']].to_csv('outfile.csv')
