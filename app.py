import os
import sys
import pandas as pd
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from networksecurity.utils.main_utils.utils import read_yaml_file, load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipelines.training_pipeline import TrainingPipeline

# Loading environment variables
load_dotenv()

SCHEMA_FILE_PATH = os.getenv("SCHEMA_FILE_PATH")
MODEL_FILE_PATH = os.getenv("MODEL_FILE_PATH")

if not SCHEMA_FILE_PATH or not MODEL_FILE_PATH:
    raise RuntimeError("SCHEMA and MODEL file path must be set.")

# Global objects
schema = None
model = None
network_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    event handler for loading artifacts.
    """
    global schema, model, network_model
    try:
        schema = read_yaml_file(SCHEMA_FILE_PATH)
        model = load_object(MODEL_FILE_PATH)
        network_model = NetworkModel(model=model)
        yield
    finally:
        pass    

app = FastAPI(
    title="Phishing URL Identifier API",
    lifespan=lifespan,
    description="API for predicting whether a given URL is malicious (i.e. phishing URL) or non-malicious.",
)

# CORS Enabled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "Welcome to the Network Security API"}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/train")
def train():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return {"message": "Training pipeline executed successfully."}
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
def predict(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        # Schema validation
        df_cols = df.columns.tolist()
        schema_cols = [list(col.keys())[0] for col in schema["columns"]]

        if "Result" in schema_cols:
            schema_cols.remove("Result")

        if df_cols != schema_cols:
            raise HTTPException(
                status_code=400,
                detail="Invalid file schema"
            )

        # Feature engineering
        df = network_model.feature_engineering(df)

        # Prediction
        prediction = model.predict(df)
        probability = model.predict_proba(df) if hasattr(model, "predict_proba") else None

        response = {}
        for i, pred in enumerate(prediction):
            confidence = None
            if probability is not None:
                confidence = {
                    "non-malicious": float(round(probability[i][0], 4)),
                    "malicious": float(round(probability[i][1], 4))
                }

            response[f"url_{i+1}"] = {
                "prediction": "malicious" if pred == 1 else "non-malicious",
                "confidence": confidence
            }

        return JSONResponse(content=response, status_code=200)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error during prediction"
        )
