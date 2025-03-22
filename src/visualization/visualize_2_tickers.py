import matplotlib.pyplot as plt
import pandas as pd

def visualize_2_tickers(df1, df2, label1="VNINDEX", label2="VN30F1M"):
    """
    Plots daily, weekly, and monthly returns of two stock market indices, ensuring common dates.

    Parameters:
    df1 (pd.DataFrame): First DataFrame containing 'DTYYYYMMDD' and return columns.
    df2 (pd.DataFrame): Second DataFrame containing 'DTYYYYMMDD' and return columns.
    label1 (str): Label for the first DataFrame (default: "VNINDEX").
    label2 (str): Label for the second DataFrame (default: "VN30F1M").
    """

    # Make copies to avoid modifying the original DataFrames
    df1_copy, df2_copy = df1.copy(), df2.copy()

    # Convert 'DTYYYYMMDD' to datetime format
    df1_copy['DTYYYYMMDD'] = pd.to_datetime(df1_copy['DTYYYYMMDD'])
    df2_copy['DTYYYYMMDD'] = pd.to_datetime(df2_copy['DTYYYYMMDD'])

    # Find common dates
    common_dates = df1_copy['DTYYYYMMDD'].isin(df2_copy['DTYYYYMMDD'])

    # Filter both DataFrames to keep only common dates
    df1_copy, df2_copy = df1_copy[common_dates], df2_copy[df2_copy['DTYYYYMMDD'].isin(df1_copy['DTYYYYMMDD'])]

    # Set 'DTYYYYMMDD' as the index
    df1_copy.set_index('DTYYYYMMDD', inplace=True)
    df2_copy.set_index('DTYYYYMMDD', inplace=True)

    # Create figure and axes
    fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)  # 3 rows, 1 column

    # Define column names and titles
    columns = ['daily_returns', 'weekly_returns', 'monthly_returns']
    titles = ['Daily Returns', 'Weekly Returns', 'Monthly Returns']

    # Plot each return type
    for i, col in enumerate(columns):
        axes[i].plot(df1_copy.index, df1_copy[col], label=label1, color='blue', linestyle='-')
        axes[i].plot(df2_copy.index, df2_copy[col], label=label2, color='red', linestyle='--')

        axes[i].set_title(titles[i])
        axes[i].legend()
        axes[i].grid(True, linestyle='--', alpha=0.6)

    # Set X-axis label as "Date"
    plt.xlabel("Date")

    # Auto-adjust layout
    plt.tight_layout()
    plt.show()
