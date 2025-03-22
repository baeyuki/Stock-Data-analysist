import pandas as pd
import sys
import os

src_path = os.path.abspath(os.path.join(os.getcwd(), "..", "src"))
sys.path.insert(0, src_path)

from get_company_names.get_VN100_company_names import get_VN100_company_names
from get_company_names.get_VN30_company_names import get_VN30_company_names

def add_features_for_group_index(df, ticker):
    # Ép kiểu Ticker về chuỗi để đảm bảo nhất quán
    df = df.copy()
    df['Ticker'] = df['Ticker'].astype(str)
    df['DTYYYYMMDD'] = pd.to_datetime(df['DTYYYYMMDD'])

    ticker_df = df[df['Ticker'] == ticker].copy().sort_values('DTYYYYMMDD')

    if ticker == 'VNINDEX':
        vn_tickers = get_VN100_company_names()
    elif ticker == 'VN30F1M':
        vn_tickers = get_VN30_company_names()
    else:
        raise ValueError("Ticker must be either 'VNINDEX' or 'VN30F1M'")

    # Ép kiểu filtered_tickers về chuỗi
    filtered_tickers = [str(t) for t in vn_tickers if str(t) in df['Ticker'].unique()]

    if not filtered_tickers:
        print(f"Warning: No tickers from {ticker} found in the DataFrame.")
        feature_cols = ['Net_advances', 'A/D', 'Schultz', 'McClellan_Oscillator', 'TRIN', 'StockAboveMA50',
                        'EMA19_net_adv', 'EMA39_net_adv'] + \
                       [f'MA{period}' for period in [5, 10, 20, 50, 100, 200]] + \
                       [f'EMA{period}' for period in [5, 10, 20, 50, 100, 200]]
        for col in feature_cols:
            ticker_df[col] = float('nan')
        return ticker_df

    # Lọc tickers_df chỉ giữ các mã trong filtered_tickers
    tickers_df = df[df['Ticker'].isin(filtered_tickers)].copy().sort_values(['Ticker', 'DTYYYYMMDD'])

    if tickers_df.empty:
        print(f"Warning: No data available for tickers from {ticker} in the DataFrame.")
        feature_cols = ['Net_advances', 'A/D', 'Schultz', 'McClellan_Oscillator', 'TRIN', 'StockAboveMA50',
                        'EMA19_net_adv', 'EMA39_net_adv'] + \
                       [f'MA{period}' for period in [5, 10, 20, 50, 100, 200]] + \
                       [f'EMA{period}' for period in [5, 10, 20, 50, 100, 200]]
        for col in feature_cols:
            ticker_df[col] = float('nan')
        return ticker_df

    # Tính giá Close trước đó (t-1) cho từng mã
    tickers_df['Close_prev'] = tickers_df.groupby('Ticker')['Close'].shift(1)
    tickers_df['Price_change'] = tickers_df['Close'] - tickers_df['Close_prev']

    # Nhóm theo ngày để tính các chỉ số
    grouped = tickers_df.groupby('DTYYYYMMDD')
    num_increasing = grouped.apply(lambda x: (x['Price_change'] > 0).sum())
    num_decreasing = grouped.apply(lambda x: (x['Price_change'] < 0).sum())
    volume_up = grouped.apply(lambda x: x.loc[x['Price_change'] > 0, 'Volume'].sum())
    volume_down = grouped.apply(lambda x: x.loc[x['Price_change'] < 0, 'Volume'].sum())

    ticker_df = ticker_df.set_index('DTYYYYMMDD')
    ticker_df['Net_advances'] = (num_increasing - num_decreasing).reindex(ticker_df.index)
    ticker_df['A/D'] = (num_increasing / num_decreasing.replace(0, float('nan'))).reindex(ticker_df.index)
    ticker_df['Schultz'] = (num_increasing / len(filtered_tickers)).reindex(ticker_df.index)

    ticker_df['EMA19_net_adv'] = ticker_df['Net_advances'].ewm(span=19, adjust=False).mean()
    ticker_df['EMA39_net_adv'] = ticker_df['Net_advances'].ewm(span=39, adjust=False).mean()
    ticker_df['McClellan_Oscillator'] = ticker_df['EMA19_net_adv'] - ticker_df['EMA39_net_adv']

    ticker_df['TRIN'] = (num_increasing / num_decreasing.replace(0, float('nan')) / 
                         (volume_up / volume_down.replace(0, float('nan')))).reindex(ticker_df.index)

    # StockAboveMA50: Chỉ tính trên các Ticker thực sự có dữ liệu
    valid_tickers = tickers_df['Ticker'].value_counts()
    valid_tickers = valid_tickers[valid_tickers > 0].index  # Chỉ giữ Ticker có dữ liệu
    valid_tickers_df = tickers_df[tickers_df['Ticker'].isin(valid_tickers)].copy()    
    valid_tickers_df['MA50'] = (valid_tickers_df.groupby('Ticker')['Close']
                                .rolling(window=50, min_periods=1)
                                .mean()
                                .reset_index(level=0, drop=True))
    valid_tickers_df['Above_MA50'] = (valid_tickers_df['Close'] > valid_tickers_df['MA50']).astype(int)
    stock_above_ma50 = valid_tickers_df.groupby('DTYYYYMMDD')['Above_MA50'].sum()
    ticker_df['StockAboveMA50'] = stock_above_ma50.reindex(ticker_df.index)

    # Tính MA và EMA cho ticker (VNINDEX hoặc VN30F1M)
    ma_periods = [5, 10, 20, 50, 100, 200]
    for period in ma_periods:
        ticker_df[f'MA{period}'] = ticker_df['Close'].rolling(window=period, min_periods=1).mean()
        ticker_df[f'EMA{period}'] = ticker_df['Close'].ewm(span=period, adjust=False).mean()

    ticker_df = ticker_df.reset_index()
    ticker_df.fillna(method='ffill', inplace=True)
    ticker_df.fillna(method='bfill', inplace=True)
    return ticker_df