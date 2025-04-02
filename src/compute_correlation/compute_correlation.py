import pandas as pd

def compute_correlation(df1,df2,cols):
    """
    Compute the correlation between two dataframes based on the specified columns.

    Args:
        df1 (pd.DataFrame): The first dataframe.
        df2 (pd.DataFrame): The second dataframe.
        cols (str): The columns to compute the correlation for, separated by commas.

    Returns:
        pd.DataFrame: A dataframe containing the correlation matrix.
    """
    new_df1 = df1.copy()
    new_df2 = df2.copy()
    new_df1.set_index('DTYYYYMMDD',inplace = True)
    new_df2.set_index('DTYYYYMMDD',inplace = True)
    cols_list = cols.split(',')
    df = pd.DataFrame()
    for col in cols_list:
        merged = pd.concat([new_df1[col], new_df2[col]], axis=1).dropna()
        corr_value = merged.iloc[:, 0].corr(merged.iloc[:, 1])
        print(f"Correlation of {col} between df1 and df2 is {corr_value}")
        df = pd.concat([merged,df],axis =1)
    corr_matrix = df.corr()
    # print(corr_matrix)    
    return corr_matrix
