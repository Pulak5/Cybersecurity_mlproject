import sys
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.components.data_ingestion import DataIngestion,DataIngestionArtifact
from networksecurity.components.data_validation import DataValidation
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
        logging.info("Data initiation completed")
        print(dataingestionconfig)
        data_validation=DataValidation(data_ingestion_artifact=DataIngestionArtifact(trained_file_path=dataingestionconfig.trained_file_path,test_file_path=dataingestionconfig.test_file_path),data_validation_config=DataValidationConfig(training_pipeline_config=train_pipe))
        logging.info("Initiate data validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
