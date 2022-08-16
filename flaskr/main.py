import json
from flask import Flask
from flask_restful import Resource, Api
from flask_apispec import marshal_with
from flask_apispec import use_kwargs
from marshmallow import fields
from marshmallow import Schema

from re import A
import time
import hmac
import pandas as pd
from requests import Request, Session
import numpy as np

# from flaskr.schema.account import Account
# from flaskr.logic.functions import getAccountFills


class Account():
    def __init__(self):  # empty initialization
        self.id = []
        self.api_key = []
        self.api_secret = []

    def add_api(self, apikey, apisecret):
        try:
            self.api_key.append(apikey)
            self.api_secret.append(apisecret)
        except Exception as e:
            print('Error adding api keys')
        return


class GetRequestSchema(Schema):
    apiKey = fields.String(default="")
    apiSecret = fields.String(default="")


arraydata = [
    {'assetName': "USD", 'balance': 7.7e-7, 'price': 1.0098591276623377,
        'symbol': "USD", 'value': 7.775915283e-7},
    {'assetName': "FTT", 'balance': 0.099734, 'price': 31.445,
        'symbol': "FTT", 'value': 3.13613563},
    {'assetName': "TRX", 'balance': 0.000003, 'price': 0.0703873,
        'symbol': "TRX", 'value': 2.111619e-7},
]


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
    # print(response)

    data = pd.DataFrame(response['result'])
    # print(data)
    # what are the unique mkts going throguh transactions
    # print((data['baseCurrency']+'/'+data['quoteCurrency']).unique())
    walletData = pd.DataFrame(arraydata)
    walletDataNoUSD = walletData[walletData['assetName'] != 'USD']
   # a = data[['baseCurrency','quoteCurrency']].isin(walletData['assetName'])

    test = pd.DataFrame()
    walletDataOnly = data.merge(
        walletDataNoUSD, how='inner', left_on='baseCurrency', right_on='assetName')
    test = walletDataOnly[walletDataOnly['side']=='buy']
    getUniqueSymbol = test['symbol'].unique()
    totalSpent = []
    totalQty = []
    for idx, i in enumerate(getUniqueSymbol):
        a = test[test['symbol']==i]
        print((a['price_x']*a['size']).sum())
        totalSpent.append((a['price_x']*a['size']).sum())
        totalQty.append(a['size'].sum())
    avgEntryPrice = [i / j for i, j in zip(totalSpent, totalQty)]
    returnDict = {walletData['assetName'][i]:  "-" for i in range(len(walletData['assetName']))}
    resultDict = {getUniqueSymbol[i]: avgEntryPrice[i] for i in range(len(getUniqueSymbol))}
    #print(resultDict)
    return returnDict


app = Flask(__name__)
api = Api(app)


class FtxApi(Resource):
    @use_kwargs(GetRequestSchema, location=("json"))
    def get(self, **kwargs):
        user_account = Account()
        # input("Please input FTX API Key:\n")
        # user_account.api_key = 'oAPx_C46gtKj-IzaOY0LK_p7t_p75kREBCLngATk'
        # input("Please input FTX API Secret:\n")
        # user_account.api_secret = 'WhRV3Ypxa08bsH_qF8w8iuVhcC-bGPbATwOK12h5'

        apiKey = kwargs.get("apiKey")
        apiSecret = kwargs.get("apiSecret")
        user_account.api_key = apiKey
        user_account.api_secret = apiSecret

        main_values = getAccountFills(
            user_account.api_key, user_account.api_secret)
        return main_values


api.add_resource(FtxApi, '/')

if __name__ == '__main__':
    app.run(debug=True)
