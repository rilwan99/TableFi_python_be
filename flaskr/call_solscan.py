from ast import parse
import requests
import json
import pandas as pd
import numpy as np
response_API = requests.get('https://public-api.solscan.io/account/splTransfers?account=Ck1b1oTDXvDDWmci5j2XCCtRQ9QmAByeGFqJLhqzoXqN&fromTime=1640995200')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
data = response_API.text
parse_json = json.loads(data)

a = pd.DataFrame(parse_json['data'])
print(a)
temp = a[['symbol', 'preBalance','postBalance', 'changeAmount','fee', 'decimals']]
# totalFees = temp['fee'].sum()

# temp[['changeAmount','fee', 'preBalance', 'postBalance']] = temp[['changeAmount','fee', 'preBalance', 'postBalance']].astype(float)
# temp['finalAmt']=temp['changeAmount']/pow(10, temp['decimals'])
# temp['maxAmt']=temp['finalAmt']

# temp_2 = temp.groupby('symbol',as_index=False).agg({'changeAmount':'sum','fee':'sum', 'preBalance':'sum', 'postBalance':'sum', 'decimals':'first', 'finalAmt':'sum', 'maxAmt':'max'})
# print(temp_2)
# avg_price = sum(temp_2.loc[temp_2['symbol']=='USDC']['maxAmt'], temp_2.loc[temp_2['symbol']=='USDT']['maxAmt'])
# print(temp_2[temp_2['symbol']=='GST']['maxAmt'])
# returnDict = {temp_2['symbol'][i]:  "-" for i in range(len(temp_2['symbol']))}
# #validDict = {temp_2['symbol'][0]:0}
# #print(temp_2['symbol'][0])
# b = temp_2.loc[temp_2['symbol']=='GST']['maxAmt']
# for i in b:
#     c = i
# for i in avg_price:
#     a = (i/c)
# validDict = {temp_2['symbol'][0]:a}
# print(validDict)
# returnDict = {temp_2['symbol'][i]:  "-" for i in range(len(temp_2['symbol']))}
# for k, v in returnDict.items():
#         if k in validDict:
#             returnDict[k] = validDict.get(k)
# print(returnDict) 
#return returnDict
#print(temp_2[temp_2['symbol']=='USDT'].maxAmt.add(temp_2[temp_2['symbol']=='USDC'].maxAmt))
#/temp_2[temp_2['symbol']=='GST']['maxAmt']

# #returnDict = {}
# returnDict = {temp_2['symbol'][i]:  "-" for i in range(len(temp_2['symbol']))}
# print(returnDict)
# print(temp_2[temp_2['symbol']=='USDC']['postBalance'])
#returnlist = []
#for i in range(0, len(temp_2)):
    # if temp_2.iloc[i]['changeAmount'] > 0:
    #     returnlist.append(temp_2[i]['changeAmount'])
    #     avg_price = ''
# print(a.groupby('symbol').count())
# a['symbol','slot','']
# import sys
# print(sys.maxsize)