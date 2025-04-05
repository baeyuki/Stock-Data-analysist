import numpy as np
import pandas as pd

class LinearRegression:
    def __init__(self):
        self.coefficients = None

    def fit(self,X,y):
        """
        Fit the linear regression model to the data
        X: numpy array of shape (10*n_samples, n_features)
        y: numpy array of shape (10*n_samples)
        """

        ## np.hstack is used to concatenate the ones column to the input data
        X = np.hstack([np.ones((X.shape[0],1)),X])
        ## solve the normal equation by least squares ( rcond=None is used to avoid division by zero)
        self.coefficients = np.linalg.lstsq(X,y,rcond=None)[0]

    def predict(self,X_new):
        """
        Predict the target values for the new data
        X_new: numpy array of shape (n_samples, n_features)
        """
        X_new = np.hstack([np.ones((X_new.shape[0],1)),X_new])
        ## @ is used for matrix multiplication
        return X_new @ self.coefficients
    def score(self, y_true, y_pred):
        """
        Calculate the R-squared score ignoring None values
        y_true: numpy array of shape (n_samples)
        y_pred: numpy array of shape (n_samples)
        """
        
        y_true = y_true[0:len(y_pred)]
        
        ## Create a mask to ignore the nan values
        mask = ~(np.isnan(y_true) | np.isnan(y_pred))
        
        ## Filter out the nan values
        y_true_clean = y_true[mask]
        y_pred_clean = y_pred[mask]
        
        ## Calculate the R-squared score
        if len(y_true_clean) > 0:
            return 1 - np.sum((y_true_clean - y_pred_clean) ** 2) / np.sum((y_true_clean - y_true_clean.mean()) ** 2)
        else:
            return None
        
        
