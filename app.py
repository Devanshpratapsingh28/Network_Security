import os
import sys
import certifi
ca = certifi.where()

import yaml
from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipelines.training_pipeline import TrainingPipeline
import pandas as pd
from networksecurity.utils.main_utils.utils import read_yaml_file, load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from networksecurity.constant.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME
)

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Welcome to the Network Security API"}


@app.get("/about")
def about():
    return {
        "message": "This API is used to predict whether given URL is malicious(i.e phishing) or benign."
    }


@app.get("/train")
def train():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return {"message": "Training pipeline executed successfully."}
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
# User Upload CSV file containing DATA is same schema as actual.
# Step - 1: User will upload CSV file.
# Step - 2: We will validate file using schema.yaml.
# Step -3 : Then we will import netwwork model and apply feature engineering then predict.
# Step - 4: Return the response as prediction to user as dictionary format like {ur11: {'prediction':'malicious',confidence:0.98},ur12:{'prediction':'benign',confidence:0.89}...}.
def predict(file: UploadFile = File(...)):
    try:
        # Step - 1: Read CSV file
        df = pd.read_csv(file.file)

        # Step - 2: Validate the file schema
        schema = read_yaml_file("data_schema/schema.yaml")
        df_cols = df.columns.tolist()
        schema_cols = [list(col.keys())[0] for col in schema["columns"]]
        # Remove target column if present
        if "Result" in schema_cols:
            schema_cols.remove("Result")
        if df_cols != schema_cols:
            raise HTTPException(status_code=400, detail="Invalid file schema")

        # Step - 3: Load model and apply feature engineering
        model = load_object("final_model/model.pkl")
        network_model = NetworkModel(model=model)

        df = network_model.feature_engineering(df)

        # Step - 4: Return the response as prediction to user as dictionary format
        predictions = model.predict(df)

        # Predict probabilities only if supported
        prediction_probs = None
        if hasattr(model, "predict_proba"):
            prediction_probs = model.predict_proba(df)

        response = {}

        for i in range(len(df)):
            response[f"url{i+1}"] = {
                "prediction": "malicious" if predictions[i] == 1 else "benign",
                "confidence": float(
                    max(prediction_probs[i]) if prediction_probs is not None else 1.0
                )
            }

        return JSONResponse(content=response, status_code=200)

    except HTTPException:
        raise

    except Exception as e:
        raise NetworkSecurityException(e, sys)
