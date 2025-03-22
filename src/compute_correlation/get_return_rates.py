import pandas as pd

def get_return_rates(df, ticker):
    # Check if ticker exists in df
    if ticker not in df['Ticker'].values:
        print(f"Ticker '{ticker}' not found in the DataFrame.")
        return pd.DataFrame()  # Return an empty DataFrame

    df_ticker = df[df['Ticker'] == ticker].copy()
    
    # Use percentage change method
    df_ticker['daily_returns'] = df_ticker['Close'].pct_change(1)
    df_ticker['weekly_returns'] = df_ticker['Close'].pct_change(7)
    df_ticker['monthly_returns'] = df_ticker['Close'].pct_change(30)

    df_ticker.fillna(method="bfill", inplace=True)

    return df_ticker

