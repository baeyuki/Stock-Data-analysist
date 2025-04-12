import pandas as pd 
import numpy as np
import os
import sys

src_path = os.path.abspath(os.path.join(os.getcwd(), "..", "src"))
sys.path.insert(0, src_path)

from models.LinearRegression import LinearRegression
from trade_stocks.trade import Trading

def hypothesisTest(data,model=None,feature_columns=None,target_column=None,financial_feature=None):
    """
    Using economic criteria to determine a model is good or bad.
    This function will return performance of an economic features (only 1 per time) , so if you want to find another feature, u can modify the trading class.
    
    Economic features :
    - Total protfit (default)
    - Total trade number
    - Win rate
    - Profit factor
    
    Args:
        data (pd.DataFrame): The list of all input data , can be in-sample or out-of-sample.
    
    """
    selected_features = []
    model = None
    target_feature = None
    financial_feature = financial_feature
    if feature_columns is None:
        selected_features = ['Net_advances','A/D','Schultz','McClellan_Oscillator']
    else:
        selected_features = feature_columns
    if model is None:
        model = LinearRegression()
    else :
        model = model()
    if target_column is None:
        target_feature = ['daily_returns']
    else:
        target_feature = target_column
    if financial_feature is not None:
        if financial_feature not in ['total_profit','total_trade_number','win_rate','profit_factor']:
            raise ValueError("The financial feature is not in the list")
    
    result = []
    for df in data:
        if df.empty:
            print("The input data is empty")
            return None, None, None, None
        ## Create new numpy array with the selected features    
        X_selected = df[selected_features].to_numpy()
        y_selected = df[target_feature].to_numpy()
        # Train the model
        len_X_selected = len(X_selected)
        # Predict the next n days
        number_of_days_to_predict = 3
        y_pred_set = [[] for _ in range(len_X_selected+number_of_days_to_predict)]

        for i in range(len_X_selected-number_of_days_to_predict):
            if i < 30:
                continue
            X_train = X_selected[(i-30):i,]
            y_train = y_selected[(i-30):i,]
            model.fit(X_train,y_train)
            y_pred = model.predict(X_selected[(i+1):(i+1+number_of_days_to_predict),])
            for j in range(number_of_days_to_predict):
                if i+j+1 < len_X_selected:
                    y_pred_set[i+j+1].append(y_pred[j])

        # Calculate the mean of the predicted values
        y_pred_set = y_pred_set[:len_X_selected]
        y_predict = []
        for i in range(len_X_selected):
            if i < 30:
                y_predict.append(np.nan)
                continue
            y_predict.append(np.mean(y_pred_set[i]))

        # Convert the predicted values to a numpy array
        y_predict = np.array(y_predict).reshape(-1,1)

        # Trading:
        trading = Trading()

        trade_signal = trading.generate_trade_signal(y_predict)
        finally_capital = trading.execute_trade(trade_signal,np.array(df['Close']))
        print("Finally capital: ", finally_capital)
        total_profit, total_trade_number, win_rate, profit_factor = trading.performance()
        
        
        if financial_feature == 'total_profit' or financial_feature is None:
            result.append(total_profit)
        elif financial_feature == 'total_trade_number':
            result.append(total_trade_number)
        elif financial_feature == 'win_rate':
            result.append(win_rate)
        elif financial_feature == 'profit_factor':
            result.append(profit_factor)
    return result 