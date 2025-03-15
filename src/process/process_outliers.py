import pandas as pd
import numpy as np
from scipy.stats import norm

def detect_outliers(df, method, column='Close', **kwargs):
    """
    Phát hiện outliers theo từng ticker.
    :param df: DataFrame chứa dữ liệu (phải có cột 'Ticker')
    :param method: Phương pháp ('threshold', 'p_value', 'second_largest')
    :param column: Cột cần kiểm tra
    :param kwargs: Các tham số bổ sung
    :return: DataFrame có thêm cột 'Outlier'
    """
    df = df.copy()
    
    def detect(group):
        if method == 'threshold':
            threshold = kwargs.get('threshold', 2)
            mean = group[column].mean()
            std = group[column].std()
            group['Outlier'] = (group[column] < mean - threshold * std) | (group[column] > mean + threshold * std)
        
        elif method == 'p_value':
            alpha = kwargs.get('alpha', 0.05)
            mean = group[column].mean()
            std = group[column].std()
            group['p_value'] = 2 * (1 - norm.cdf(np.abs(group[column] - mean) / std))
            group['Outlier'] = group['p_value'] < alpha
        
        elif method == 'second_largest':
            lookback = kwargs.get('lookback', 30)
            factor = kwargs.get('factor', 2)
            outliers = []
            for i in range(len(group)):
                if i < lookback:
                    outliers.append(False)
                else:
                    past_values = group[column].iloc[i - lookback:i]
                    largest_values = past_values.nlargest(2).values
                    smallest_values = past_values.nsmallest(2).values
                    if len(largest_values) < 2 or len(smallest_values) < 2:
                        outliers.append(False)
                    else:
                        second_largest = largest_values[1]
                        second_smallest = smallest_values[1]
                        current_value = group[column].iloc[i]
                        is_outlier = (current_value > factor * second_largest) or (current_value < second_smallest / factor)
                        outliers.append(is_outlier)
            group['Outlier'] = outliers
        
        return group
    
    return df.groupby('Ticker', group_keys=False).apply(detect)


def process_outliers(df, method, column='Close', **kwargs):
    """
    Xử lý outliers theo từng ticker.
    :param df: DataFrame chứa dữ liệu đã có cột 'Outlier'
    :param method: Phương pháp ('cap', 'discard', 'replace_second_largest')
    :param column: Cột cần xử lý
    :param kwargs: Các tham số bổ sung
    :return: DataFrame đã xử lý outliers
    """
    df = df.copy()
    if 'Outlier' not in df:
        raise ValueError("DataFrame chưa có cột 'Outlier'. Hãy chạy detect_outliers trước.")

    def process(group):
        if method == 'cap':
            lower_cap = kwargs.get('lower_cap', group[column].quantile(0.05))
            upper_cap = kwargs.get('upper_cap', group[column].quantile(0.95))
            group.loc[group['Outlier'] & (group[column] < lower_cap), column] = lower_cap
            group.loc[group['Outlier'] & (group[column] > upper_cap), column] = upper_cap

        elif method == 'discard':
            group = group[~group['Outlier']]

        elif method == 'replace_second_largest':
            lookback = kwargs.get('lookback', 30)
            factor = kwargs.get('factor', 2)
            for i in range(len(group)):
                if i >= lookback and group['Outlier'].iloc[i]:
                    past_values = group[column].iloc[i - lookback:i]
                    largest_values = past_values.nlargest(2).values
                    smallest_values = past_values.nsmallest(2).values
                    if len(largest_values) >= 2 and len(smallest_values) >= 2:
                        second_largest = largest_values[1]
                        second_smallest = smallest_values[1]
                        current_value = group[column].iloc[i]
                        if current_value > factor * second_largest:
                            group.loc[i, column] = second_largest
                        elif current_value < second_smallest / factor:
                            group.loc[i, column] = second_smallest
        return group

    return df.groupby('Ticker', group_keys=False).apply(process)
