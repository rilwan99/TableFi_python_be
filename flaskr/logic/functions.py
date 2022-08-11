from re import A
import time
import hmac
import pandas as pd
from requests import Request, Session
import numpy as np

# can omit if data is passed in?
arraydata = (
    {'assetName': "USD", 'balance': 7.7e-7, 'price': 1.0098591276623377,
        'symbol': "USD", 'value': 7.775915283e-7},
    {'assetName': "FTT", 'balance': 0.099734, 'price': 31.445,
        'symbol': "FTT", 'value': 3.13613563},
    {'assetName': "TRX", 'balance': 0.000003, 'price': 0.0703873,
        'symbol': "TRX", 'value': 2.111619e-7},
)


def sumOf(df):
    df['total'] = df['price_x'] * df['size']
    df['token_qty'] = np.where(
        df['side'] == 'sell', df['size']*(-1)-df['fee'], df['size']-df['fee'])
    df['total_value'] = np.where(
        df['side'] == 'sell', df['total'], df['total']*(-1))
    return df


def getAccountFills(api_key, api_secret):  # take in array instead?
    # take in array from previous api call
    ######################################################
    ts = int(time.time() * 1000)
    request = Request('GET', 'https://ftx.com/api/fills')
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(api_secret.encode(),
                         signature_payload, 'sha256').hexdigest()

    prepared.headers['FTX-KEY'] = api_key
    prepared.headers['FTX-SIGN'] = signature
    prepared.headers['FTX-TS'] = str(ts)

    s = Session()
    response = s.send(prepared).json()

    data = pd.DataFrame(response['result'])
    # print(data)
    # what are the unique mkts going throguh transactions
    print((data['baseCurrency']+'/'+data['quoteCurrency']).unique())
    walletData = pd.DataFrame(arraydata)
    walletDataNoUSD = walletData[walletData['assetName'] != 'USD']
   # a = data[['baseCurrency','quoteCurrency']].isin(walletData['assetName'])

    # take records that are matched with what is currently in the wallet
    walletDataOnly = data.merge(
        walletDataNoUSD, how='inner', left_on='baseCurrency', right_on='assetName')
    walletDataOnly2 = data.merge(
        walletDataNoUSD, how='inner', left_on='quoteCurrency', right_on='assetName')
    walletDataMerged = walletDataOnly.append(
        walletDataOnly2, ignore_index=False)

    walletDataMerged['joined_pairs'] = walletDataMerged['baseCurrency'] + \
        '/'+walletDataMerged['quoteCurrency']
    print(walletDataMerged)
    values = sumOf(walletDataMerged)
    valuesSum = values.sum()
    valuesSum['avgPrice'] = valuesSum['total_value']/valuesSum['token_qty']
    if valuesSum['total_value'] > 0:
        # valuesSum['finalPriceSpent']=values[values['side']=='buy'].sum()#+valuesSum['total_value']
        valuesSum['finalPriceSpent'] = values[values['side'] ==
                                              'buy']['total_value'] * -1 - valuesSum['total_value']
        # print(valuesSum['finalPriceSpent'])
    if valuesSum['token_qty'] > 0:
        valuesSum['finalQtyBought'] = values[values['side']
                                             == 'buy']['size'] - valuesSum['token_qty']
    valuesSum['avgPrice'] = valuesSum['finalPriceSpent'] / \
        valuesSum['finalQtyBought']
    print([values['symbol'][0], valuesSum['avgPrice']])

    return [values['symbol'][0], valuesSum['avgPrice']]
