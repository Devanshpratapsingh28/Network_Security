# 🛡️ Phishing URL Detection: End-to-End MLOps Pipeline

## 📖 About
This project is a production-grade machine learning system designed to identify malicious URLs. It implements a complete MLOps lifecycle from raw data ingestion from database to a containerized FastAPI deployment on AWS. The system utilizes modular pipeline components to ensure scalability, reproducibility, and rigorous data validation. In addition to binary classification, the model provides a confidence score indicating the probability of a URL being phishing, enabling more informed and reliable decision-making.

## 📊 Dataset
The dataset is sourced from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Phishing+Websites). It consists of thousands of URLs characterized by **30 distinct features** (e.g., SSL state, URL length, prefix/suffix, domain age). The target variable classifies each URL as either **Legitimate** or **Phishing**.

## 🔗 API Reference
The API is deployed on AWS EC2 and can be accessed using FastAPI’s Swagger UI:
👉 **[Interactive API Documentation](http://16.170.205.221:8000/docs)**

## 🐳 Docker Image
The application is containerized using Docker and is publicly available on Docker Hub:

- **Image Name:** `devanshdkr28/phishingidentifier-api`
- **Tag:** `1.0`

#### ▶️ Run Using Docker
You can pull and run the API locally using the following steps:

##### Pull and Run the Docker Image
```bash
docker pull devanshdkr28/phishingidentifier-api:1.0
docker run -d -p 8000:8000 devanshdkr28/phishingidentifier-api:1.0
```
##### Access the API
```bash
http://localhost:8000/docs
```

---

## 🛠️ Tech Stack

| Category           | Technologies |
|--------------------|--------------|
| Language           | Python |
| Libraries          | pandas, numpy, scikit-learn, matplotlib, seaborn |
| Backend            | FastAPI |
| Environment        | Jupyter Notebook |
| Version Control    | Git, GitHub |
| MLOps Tools        | Docker (containerization), MLflow (experiment tracking), Dagshub (remote MLflow repository) |
| Cloud Platform     | AWS (S3 Bucket for artifact storage, EC2 for API deployment) |

---

## 🏗️ System Architecture & Workflow
The core of this project is a decoupled, modular architecture where each stage produces versioned artifacts and logs metadata for full traceability.



### 1. Data Ingestion & Validation
* **Source:** Extracts raw URL records from **MongoDB** (or local CSV).
* **Feature Store:** Writes normalized datasets to local artifacts and syncs with **AWS S3**.
* **Schema Enforcement:** Validates features against a strict `schema.yaml`. Records failing validation are quarantined to ensure data drift is caught early.

### 2. Transformation & Engineering
* **Preprocessing:** Applied Feature Engineering and perform feature selection using correlation, feature extraction etc.
* **Artifacts:** Saves transformation objects (pickles) to ensure consistent preprocessing during both training and real-time inference.

### 3. Model Training & Experiment Tracking
* **Algorithms:** Evaluates multiple Scikit-learn classifiers using stratified splits.
* **Tracking:** All metrics (F1-Score, Precision, Recall) and model parameters are logged to **MLflow** and integrated with **DagsHub** for remote experiment management.
* **Model Signature:** Inferred signatures ensure the API receives data in the exact expected format.

### 4. Deployment & Orchestration
* **API:** High-performance **FastAPI** wrapper for the model.
* **Containerization:** Fully Dockerized environment to ensure "run-anywhere" consistency.
* **Deployment:** Deployed on **AWS EC2**, exposing a `/predict` endpoint for batch processing.

---

## 📂 Project Structure
```text
├── data_schema/            # YAML definitions for data validation
├── networksecurity/
│   ├── components/         # Modular pipeline stages (Ingestion ->Validation ->Transformation ->Trainer)
│   ├── entity/             # Data objects for Config and Artifacts
│   ├── pipelines/          # Training pipeline orchestrators
│   ├── cloud/              # AWS S3 synchronization logic
│   └── utils/              # Common helpers and ML specific logic
├── Artifacts/              # Local store for intermediate data/outputs
├── saved_models/           # Saved models for prediction
└── app.py                  # FastAPI entry point
```

## 🚀 Installation & Usage

1. Set Up Environment:
   ```bash
   # Clone the repository
   git clone [https://github.com/Devanshpratapsingh28/Network_Security.git](https://github.com/Devanshpratapsingh28/Network_Security.git)
   cd Network_Security

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Configure MongoDB:
   - Ensure MongoDB is running and accessible. 

3. Configure AWS S3:
   - Set up AWS credentials for S3 access.

4.  Create `.env` file:
   ```env
   SCHEMA_FILE_PATH=data_schema/schema.yaml
   MODEL_FILE_PATH=saved_models/model.pkl
   MONGODB_URI=your_mongodb_connection_string
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   S3_BUCKET_NAME=your_s3_bucket_name
   
   ```
5. Run the Training Pipeline:
   ```bash
   python main.py
   ```
6. Predict via FastAPI:
   ```bash
   uvicorn app:app --reload
   ```

Note : 
If you want to run the project using Docker, make sure to have Docker installed and run the following command to build and start the container:
```bash
docker build -t phishing-url-detector .
docker run -d -p 8000:8000 phishing-url-detector
```
---


![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit--learn](https://img.shields.io/badge/Scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)
![Dagshub](https://img.shields.io/badge/Dagshub-3B82F6?style=for-the-badge&logo=gitlab&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---
