import os
import pandas as pd

FolderPath = os.getcwd() + "/Nexus/configs/"
TokenMapPath = f"{FolderPath}aone.json"
df = pd.read_json(TokenMapPath)


def GetExchangeAndSegment(SYMBOL):
    if SYMBOL == 'SENSEX':
        exch_seg = 'BFO'
        instrumenttype = 'OPTIDX'

    elif SYMBOL == 'CRUDEOIL':
        exch_seg = 'MCX'
        instrumenttype = 'OPTFUT'
        
    else:
        exch_seg = 'NFO'
        instrumenttype = 'OPTIDX'

    return [exch_seg, instrumenttype]


def GetAoneTokenInfo(SYMBOL, CEPE, SP):

    ExchangeAndSegment = GetExchangeAndSegment(SYMBOL)
    exch_seg = ExchangeAndSegment[0]
    instrumenttype = ExchangeAndSegment[1]

    SP = SP * 100

    if exch_seg == 'NSE':
        eq_df = df[(df['exch_seg'] == 'NSE') & (df['symbol'].str.contains('EQ'))]
        return eq_df[eq_df['name'] == SYMBOL]
    
    elif exch_seg == 'NFO' and (instrumenttype in ['FUTSTK', 'FUTIDX']):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == SYMBOL)].sort_values(by=['expiry'])
    
    elif exch_seg == 'NFO' and instrumenttype in ['OPTSTK', 'OPTIDX']:
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == SYMBOL) & (df['strike'] == SP) & (df['symbol'].str.endswith(CEPE))].sort_values(by=['expiry'])
    
    elif exch_seg == 'BFO':
        return df[(df['exch_seg'] == 'BFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == SYMBOL) & (df['strike'] == SP) & (df['symbol'].str.endswith(CEPE))].sort_values(by=['expiry'])
    
    elif exch_seg == 'MCX' and (instrumenttype == 'OPTFUT'):
        return df[(df['exch_seg'] == 'MCX') & (df['instrumenttype'] == instrumenttype) & (df['name'] == SYMBOL) & (df['strike'] == SP) & (df['symbol'].str.endswith(CEPE))].sort_values(by=['expiry'])

