import pandas as pd
from datetime import datetime,timedelta


def add_features_for_specific_company(df,ticker):
    ticker_df = df[df['Ticker']==ticker].copy()
    if ticker_df.empty:
        print(f'{ticker} is not in df')
        return pd.DataFrame()

    # Add MA features
    MA_index = [5,10,20,50,100,200]
    for index in MA_index:
        ticker_df[f'MA{index}'] = ticker_df['Close'].rolling(window=index).mean()

    # Add EMA features
    EMA_index = [5,10,20,50,100,200]

    # Apply it follow the formula but it will get error cause the first one cant be caculated
    # for index in EMA_index:
    #     alpha = 2 / (index + 1)
    #     ticker_df[f'EMA{index}'] = ticker_df['Close']*alpha + ticker_df[f'EMA{index}'].shift(1)*(1-alpha)

    # Using this method instead
    for index in EMA_index:
        ticker_df[f'EMA{index}'] = df['Close'].ewm(span=index, adjust=False).mean()

    # Fill NaN values
    ticker_df.fillna(method = 'bfill',inplace = True)   
    
    return ticker_df