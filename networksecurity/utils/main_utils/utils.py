import os
import sys
import yaml
import numpy as np
import dill
import pickle

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger

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

        
