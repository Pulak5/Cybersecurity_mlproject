import sys
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

if __name__=="__main__":
    try:
        train_pipe=TrainingPipelineConfig()
        dataingconfig=DataIngestionConfig(training_pipeline_config=train_pipe)
        obj=DataIngestion(data_ingestion_config=dataingconfig)
        logging.info("Initaiting data ingestion")
        dataingestionconfig=obj.initiate_data_ingestion()
        print(dataingestionconfig)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
