from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__ == "__main__":
    try:
        tpc = TrainingPipelineConfig()
        dic = DataIngestionConfig(tpc)
        data_ingestion = DataIngestion(dic)
        logging.info("Initiate the Data Ingestion")
        dia = data_ingestion.initiate_data_ingestion()
        print(dia)
    except Exception as e:
        raise NetworkSecurityException(e,sys)    