import pandas as pd

def process_missing_data(file_data, method = None):
    """
    Xử lý dữ liệu thiếu bằng cách chọn phương pháp điền dữ liệu.
    
    :param file_data: Đường dẫn file CSV chứa dữ liệu chứng khoán
    :param method: Phương pháp điền dữ liệu (hàm xử lý)
    :return: DataFrame đã xử lý dữ liệu thiếu
    """
    # Đọc file CSV và chuyển cột ngày về kiểu datetime
    df = pd.read_csv(file_data, sep='\t')
    date_column_name = 'DTYYYYMMDD' if 'DTYYYYMMDD' in df.columns else 'date'
    df[date_column_name] = pd.to_datetime(df[date_column_name], format='%Y%m%d', errors='coerce')
    df = df.dropna(subset=[date_column_name])

    # Các phương pháp xử lý dữ liệu thiếu
    def fill_as_0(df_filled):
        df_filled.iloc[:, 1:] = df_filled.iloc[:, 1:].fillna(0)
        return df_filled

    def fill_as_mean(df_filled):
        df_filled.iloc[:, 1:] = df_filled.iloc[:, 1:].fillna(df_filled.mean(numeric_only=True))
        return df_filled

    def fill_as_median(df_filled):
        df_filled.iloc[:, 1:] = df_filled.iloc[:, 1:].fillna(df_filled.median(numeric_only=True))
        return df_filled

    def fill_as_mode(df_filled):
        df_filled.iloc[:, 1:] = df_filled.iloc[:, 1:].fillna(df_filled.mode().iloc[0])
        return df_filled

    def fill_as_ffill(df_filled):
        df_filled.iloc[:, 1:] = df_filled.iloc[:, 1:].fillna(method='ffill')
        return df_filled

    def fill_as_interpolate(df_filled):
        df_filled.iloc[:, 1:] = df_filled.iloc[:, 1:].interpolate(method='time')
        return df_filled

    def fill_as_extrapolation(df_filled):
        df_filled.iloc[:, 1:] = df_filled.iloc[:, 1:].interpolate(method='linear', limit_direction='both')
        return df_filled
    
    if method == None:
        method = fill_as_extrapolation

    # Hàm điền dữ liệu thiếu theo từng mã cổ phiếu
    def fill_missing_data(ticker, df, method):
        """Điền dữ liệu thiếu theo từng mã cổ phiếu (Ticker)"""
        df_ticker = df[df['Ticker'] == ticker].copy()

        # Tạo chuỗi ngày đầy đủ từ ngày nhỏ nhất đến ngày lớn nhất
        full_dates = pd.date_range(df_ticker[date_column_name].min(), df_ticker[date_column_name].max(), freq='B')  
        full_df = pd.DataFrame({date_column_name: full_dates})
        
        df_filled = full_df.merge(df_ticker, on=date_column_name, how='left')

        # Áp dụng phương pháp điền dữ liệu thiếu
        df_filled = method(df_filled)

        # Điền lại 'Ticker' bằng forward-fill
        df_filled['Ticker'] = df_filled['Ticker'].ffill()

        return df_filled

    # Áp dụng cho từng mã cổ phiếu
    df_list = [fill_missing_data(ticker, df, method) for ticker in df['Ticker'].dropna().unique()]
    df = pd.concat(df_list, ignore_index=True)

    print("Done! Missing data has been filled using the selected method.")
    
    return df


