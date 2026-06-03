import sys
import os
import certifi
ca=certifi.where()
from fastapi.responses import HTMLResponse


from dotenv import load_dotenv
load_dotenv()
mongodb_url=os.getenv("MONGODB_URL")
import pymongo
from pymongo.server_api import ServerApi
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.constant.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")
import pandas as pd

client=pymongo.MongoClient(mongodb_url,server_api=ServerApi('1'))
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")
@app.get("/train")
async def train_route():
    try:
        training_pipeline=TrainingPipeline()
        model_trainer_artifact=training_pipeline.run_pipeline()
        return Response("Training is sucessful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object(os.path.join("final_models","preprocessor.pkl"))
        final_model=load_object(os.path.join("final_models","model.pkl"))
        print("PREPROCESSOR =", preprocesor)
        print("MODEL =", final_model)

        print("PREPROCESSOR TYPE =", type(preprocesor))
        print("MODEL TYPE =", type(final_model))
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        # print(df.iloc[0])
        y_pred = network_model.predict(df)
        # print(y_pred)
        df['predicted_column'] = y_pred
        # print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return HTMLResponse(content=table_html)

        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
