from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__ == "__main__":
    try:
        tpc = TrainingPipelineConfig()
        dic = DataIngestionConfig(tpc)
        data_ingestion = DataIngestion(dic)
        logging.info("Initiate the Data Ingestion")
        dia = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        print(dia)
        dvc = DataValidationConfig(tpc)
        data_validation = DataValidation(dia,dvc)
        logging.info("Initiate the Data Validation")
        dva = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(dva)
        dtc = DataTransformationConfig(tpc)
        data_transformation = DataTransformation(dva,dtc)
        logging.info("Initiate the Data Transformation")
        dta = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(dta)
    except Exception as e:
        raise NetworkSecurityException(e,sys)    