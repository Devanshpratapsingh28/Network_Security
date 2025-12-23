import os
import sys
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def create_feature(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df['url_obfuscation_score'] = df['Shortining_Service'] + df['double_slash_redirecting'] + df['having_At_Symbol'] + df['Prefix_Suffix']
            df['ui_deception_score'] = df['on_mouseover'] + df['RightClick'] + df['popUpWidnow'] + df['Iframe']
            df['trust_score'] = df['SSLfinal_State'] + df['HTTPS_token'] + df['Google_Index']
            df['redirection_risk_score'] = df['Redirect'] + df['Submitting_to_email'] + df['Abnormal_URL']
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def drop_features(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            excluded_features = [
                'Shortining_Service','double_slash_redirecting','having_At_Symbol','Prefix_Suffix',
                'on_mouseover','RightClick','popUpWidnow','Iframe',
                'SSLfinal_State','HTTPS_token','Google_Index',
                'Redirect','Submitting_to_email','Abnormal_URL',
                'URL_Length','Domain_registeration_length','Favicon','port',
                'Links_in_tags','SFH','age_of_domain','DNSRecord',
                'Page_Rank','Links_pointing_to_page','Statistical_report'
            ]
            dataframe = dataframe.drop(columns=excluded_features, axis=1)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def feature_engineering(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            # Step - 1 : Replacing -1 with 0.
            dataframe = dataframe.replace(-1, 0)

            # Step - 2 : Filling missing values with 0.
            for col in dataframe.columns:
                if col != "Result":
                    dataframe[col] = dataframe[col].fillna(0)

            # Step - 3 : Creating new features.
            dataframe = self.create_feature(dataframe)

            # Step - 4 : Dropping correlated features.
            dataframe = self.drop_features(dataframe)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self):  
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")

            train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            # Applying Feature Engineering
            logging.info("Applying Feature Engineering on training and testing dataframe")
            train_df = self.feature_engineering(train_df)
            test_df = self.feature_engineering(test_df)
            logging.info("Feature Engineering applied successfully")
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_train_file_path), exist_ok=True)

            train_df.to_csv(self.data_transformation_config.transformed_train_file_path, index=False)
            test_df.to_csv(self.data_transformation_config.transformed_test_file_path, index=False)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
