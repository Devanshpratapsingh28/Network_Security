from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os
import sys
import numpy as np
import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.ml_utils.feature_engineering import feature_engineering

class NetworkModel:
    def __init__(self,model):
        try:
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            y_pred = self.model.predict(x)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def feature_engineering(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return feature_engineering(dataframe)