import sys
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,TrainingPipelineConfig,ModelTrainerConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.logging.logger import logging

if __name__=="__main__":
    try:
        train_pipe=TrainingPipelineConfig()
        dataingconfig=DataIngestionConfig(training_pipeline_config=train_pipe)
        obj=DataIngestion(data_ingestion_config=dataingconfig)
        logging.info("Initaiting data ingestion")
        dataingestionartifact=obj.initiate_data_ingestion()
        logging.info("Data initiation completed")
        print(dataingestionartifact)
        data_validation=DataValidation(data_ingestion_artifact=dataingestionartifact,data_validation_config=DataValidationConfig(training_pipeline_config=train_pipe))
        logging.info("Initiate data validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)
        data_transformation_config=DataTransformationConfig(training_pipeline_config=train_pipe)
        data_transformation=DataTransformation(data_transformation_config,data_validation_artifact)
        logging.info("Initiating data transformation")
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed")
        print(data_transformation_artifact)

        logging.info("Model Training started")
        model_trainer_config=ModelTrainerConfig(training_pipeline_config=train_pipe)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("Model Training artifact created")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
