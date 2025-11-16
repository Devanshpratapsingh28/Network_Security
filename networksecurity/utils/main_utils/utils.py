import os
import sys
import yaml
import numpy as np
import pickle
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

def read_yaml_file(file_path):
    try :
        with open(file=file_path, mode="rb" ) as file:
            return yaml.safe_load(file) # Returning as dictionary
    except Exception as e:
        raise NetworkSecurityException(e,sys)    
    
def write_yaml_file(file_path, content, replace = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of main_Utils/utils file.")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of main_Utils/utils file.")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e  

def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        best_estimators = {}

        for model_name, model in models.items():

            param_grid = params[model_name]

            gs = GridSearchCV(
                model,
                param_grid,
                scoring="f1",
                cv=3,
                n_jobs=-1,
                verbose=1
            )
            gs.fit(X_train, y_train)

            best_model = gs.best_estimator_

            y_test_pred = best_model.predict(X_test)

            test_score = f1_score(y_test, y_test_pred)

            report[model_name] = test_score
            best_estimators[model_name] = best_model

        return report, best_estimators

    except Exception as e:
        raise NetworkSecurityException(e, sys)
