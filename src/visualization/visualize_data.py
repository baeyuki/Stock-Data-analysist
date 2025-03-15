import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_data(df, ticker, date_column_name='DTYYYYMMDD', start_date='2025-01-01', end_date=None):
    """
    Vẽ biểu đồ dữ liệu của mã cổ phiếu (Ticker).
    
    Params:
    - df: DataFrame chứa dữ liệu cổ phiếu
    - ticker: Mã cổ phiếu cần vẽ biểu đồ
    - date_column_name: Tên cột chứa ngày
    - start_date: Ngày bắt đầu (default: '2025-01-01')
    - end_date: Ngày kết thúc (default: ngày cuối cùng trong dữ liệu)
    
    Returns:
    - df_ticker: DataFrame chứa dữ liệu đã lọc theo ticker & thời gian
    """

    if end_date is None:
        end_date = df[date_column_name].max()  # Lấy ngày lớn nhất trong dataset

    # Lọc dữ liệu theo ticker và khoảng thời gian
    df_ticker = df[(df['Ticker'] == ticker) & 
                   (df[date_column_name] >= start_date) & 
                   (df[date_column_name] <= end_date)].copy()

    # Vẽ biểu đồ bằng Seaborn
    plt.figure(figsize=(15, 5))
    sns.set_style("whitegrid")

    for col in ['Open', 'High', 'Low', 'Close']:
        if col in df_ticker.columns:
            plt.plot(df_ticker[date_column_name], df_ticker[col], marker='o', markersize=3, label=col)

    plt.title(f"Diễn biến giá cổ phiếu: {ticker}", fontsize=14)
    plt.xlabel("Ngày", fontsize=12)
    plt.ylabel("Giá cổ phiếu", fontsize=12)
    plt.legend(loc='upper left')
    plt.xticks(rotation=45)  # Xoay nhãn ngày
    plt.tight_layout()
    plt.show()

    return df_ticker.head()
