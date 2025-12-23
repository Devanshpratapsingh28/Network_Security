import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
import pandas as pd

class DataValidation:
    
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_number_of_cols(self,df:pd.DataFrame):
        try:
            schema_columns = [list(col.keys())[0] for col in self.schema_config["columns"]]
            no_of_cols = len(schema_columns)
            df_cols_len = len(df.columns)
            logging.info(f"Required columns length : {no_of_cols}")
            logging.info(f"DataFrame columns length : {df_cols_len}")
            if df_cols_len == no_of_cols:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_col_names(self, df: pd.DataFrame):
        schema_columns = [list(col.keys())[0] for col in self.schema_config["columns"]]
        df_columns = list(df.columns)
        return schema_columns == df_columns

    def initiate_data_validation(self) -> DataValidationArtifact:
        try :
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read the data from train and test
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            invalid_report = {}

            # Validating with number of columns and actual column names.
            schema_invalid_train = False
            status = self.validate_number_of_cols(train_df)
            if not status:
                error_message = "Train dataframe does not have same number of columns as desired schema."
                logging.error(error_message)
                invalid_report["train"] = error_message
                schema_invalid_train = True

            if not schema_invalid_train:
                status = self.validate_col_names(train_df)    
                if not status:
                    error_message = "Train dataframe does not match the required schema either wrong columns are their or columns order differ the actual schema."
                    logging.error(error_message)
                    invalid_report["train"] = error_message
                    schema_invalid_train = True

            schema_invalid_test = False
            status = self.validate_number_of_cols(test_df)
            if not status:
                error_message = "Test dataframe does not have same number of columns as desired schema."
                logging.error(error_message)
                invalid_report["test"] = error_message
                schema_invalid_test = True

            if not schema_invalid_test:
                status = self.validate_col_names(test_df)  
                if not status:
                    error_message = "Test dataframe does not match the required schema either wrong columns are their or columns order differ the actual schema."
                    logging.error(error_message)
                    invalid_report["test"] = error_message
                    schema_invalid_test = True

            if schema_invalid_train or schema_invalid_test:
                invalid_dir = os.path.dirname(self.data_validation_config.invalid_report_file_path)
                os.makedirs(invalid_dir, exist_ok=True)
                write_yaml_file(file_path=self.data_validation_config.invalid_report_file_path,content=invalid_report)
                raise NetworkSecurityException("Schema validation failed. See invalid report for details.",sys)

            status = True  

            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)

            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status, 
                valid_train_file_path=self.data_validation_config.valid_train_file_path,  
                valid_test_file_path=self.data_validation_config.valid_test_file_path,    
                invalid_report_file_path=self.data_validation_config.invalid_report_file_path
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
