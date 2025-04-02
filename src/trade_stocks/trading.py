import pandas as pd
import numpy as np

class Trading:
    def __init__(self,initial_capital = 2000000,trade_size = 10,fee_rate = 0.001):
        self.initial_capital = initial_capital
        self.trade_size = trade_size
        self.fee_rate = fee_rate
        self.current_capital = initial_capital
        self.current_position = 0
    def generate_trade_signal(self,y_predicted):
        """
        Generate trade signals based on predicted values.

        Args:
            y_predicted (np.ndarray): Predicted values from the model.

        Returns:
            pd.Series: Trade signals (1 for buy, -1 for sell, 0 for hold).
        """
        trade_signal = np.zeros(len(y_predicted))
        for i in range(1, len(y_predicted)):
            if y_predicted[i] > y_predicted[i-1]:
                trade_signal[i] = 1
            elif y_predicted[i] < y_predicted[i-1]:
                trade_signal[i] = -1
        return trade_signal
    
    def execute_trade(self,trade_signal,prices):
        """
        Execute trades based on the trade signal.

        Args:
            trade_signal (np.ndarray): Trade signals (1 for buy, -1 for sell, 0 for hold).
            prices (np.ndarray): Prices of the stock.
        """
        entry_price = 0
        exit_price = 0
        for i in range(len(trade_signal)):
            if self.current_position == 0:
                if trade_signal[i] == 1:
                    entry_price = prices[i]
                    self.current_position += 1
                else:
                    if trade_signal[i] == -1:
                        entry_price = prices[i]
            elif self.current_position == 1:
                if trade_signal[i] == -1:
                    exit_price = prices[i]
                    self.current_position -= 1
                    self.current_capital += (exit_price - entry_price) * self.trade_size - self.fee_rate * self.trade_size
                    entry_price = 0
            else:
                if trade_signal[i] == 1:
                    entry_price = prices[i]
                    self.current_position += 1
                else:
                    exit_price = prices[i]
                    self.current_position -= 1

        
