from ast import parse
import requests
import json
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

time = '1640995200' #using 1 april 2022
walletPublicKey = 'Ck1b1oTDXvDDWmci5j2XCCtRQ9QmAByeGFqJLhqzoXqN'
url = 'https://public-api.solscan.io/account/splTransfers?account='

requestString = url + walletPublicKey + '&fromTime=' + time
print(requestString)

response_API = requests.get(requestString) #takes last 10 txn per public API
#response_API = requests.get('https://public-api.solscan.io/account/splTransfers?account=Ck1b1oTDXvDDWmci5j2XCCtRQ9QmAByeGFqJLhqzoXqN&fromTime=1640995200')
stablecoins = ['USDC', 'USDT']

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
data = response_API.text
parse_json = json.loads(data)

a = pd.DataFrame(parse_json['data'])

#take max amt to avg out price
temp = a[['symbol', 'preBalance','postBalance', 'changeAmount','fee', 'decimals']]
totalFees = temp['fee'].sum()

temp[['changeAmount','fee', 'preBalance', 'postBalance']] = temp[['changeAmount','fee', 'preBalance', 'postBalance']].astype(float)
temp['finalAmt']=temp['changeAmount']/pow(10, temp['decimals'])
temp['maxAmt']=temp['finalAmt']
walletDataNoUSD = temp[~temp['symbol'].isin(stablecoins)]  #remove stablecoins

temp_2 = temp.groupby('symbol',as_index=False).agg({'changeAmount':'sum','fee':'sum', 'preBalance':'sum', 'postBalance':'sum', 'decimals':'first', 'finalAmt':'sum', 'maxAmt':'max'})
stablecoinsAmt = temp_2.loc[temp_2['symbol'].isin(stablecoins)]['maxAmt'].sum()
returnDict = {temp_2['symbol'][i]:  "-" for i in range(len(temp_2['symbol']))}
walletTokenMaxAmt = temp_2[temp_2['symbol'].isin(walletDataNoUSD['symbol'])]['maxAmt']
getUniqueSymbol = walletDataNoUSD['symbol'].unique()
avgEntryPrice = []
for idx, i in enumerate(getUniqueSymbol):
    avgEntryPrice.append(stablecoinsAmt/walletTokenMaxAmt[idx])
resultDict = {getUniqueSymbol[i]: avgEntryPrice[i] for i in range(len(getUniqueSymbol))}
print(resultDict)
#return resultDict