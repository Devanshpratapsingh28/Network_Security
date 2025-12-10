1. Project Structure : 
    - Network-Data,networksecurity,notebooks,venv,requirements.txt,.env,.gitignore

2. `setup.py`
3. `networksecurity/logging/logger.py`
4. `networksecurity/exception/exception.py`
5. Data - Ingestion Pipeline Building : `constant(training_pipeline/__init__) -> entity(config_entity,artifact_entity) -> components(data_ingestion.py)`.
6. Data - Validation Pipeline Building : `constant(training_pipeline/__init__),utils/main_utils/utils.py,data_schema/schema.yaml -> entity(config_entity,artifact_entity) -> components(data_validation.py)`.
7. Data - Transformation Pipeline Building : `constant(training_pipeline/__init__),utils/main_utils/utils.py -> entity(config_entity,artifact_entity) -> components(data_transformation.py)`.
8. Model - Trainer : `constant(training_pipeline/__init__),utils/main_utils/utils.py -> entity(config_entity,artifact_entity) -> components(model_trainer.py)`. We also integrated mlflow with dagshub for model tracking and logging.
9. AWS S3 Bucket : `constant(training_pipeline/__init__),utils/main_utils/utils.py -> entity(config_entity,artifact_entity) -> components(s3_bucket.py)`.




## Errors that I got:
1. Compaltibility error between mlflow and dagshub.
    - Description: While integrating mlflow with dagshub, I encountered compatibility issues that prevented seamless logging and tracking of machine learning experiments.It was beacause of version mismatch, as dagshub required an older version of mlflow.
    - Solution: I resolved this by downgrading mlflow to version 2.9.2, which is compatible with dagshub. This allowed me to successfully log models and metrics to dagshub without any further compatibility issues.

 2. Buster image error in Dockerfile.
    - Reason : While building the Docker image, I encountered errors related to the 'buster' image. This was due to the deprecation of the 'buster' tag in favor of more recent versions of the base image.
    - Solution: I resolved this by updating the Dockerfile to use the 'bullseye' tag instead of 'buster'. This change ensured that I was using a supported and up-to-date base image, allowing the Docker build process to complete successfully.   


## FastAPI run command:
`uvicorn app:app --host localhost --port 8000 --reload`

## AWS Configuration Command:
First, you need to configure your AWS credentials to allow the application to access AWS services like S3. Create S3 bucket and configure your AWS credentials using the following command:

```bash
aws configure
```
## apt vs apt-get :
- Both do the same job → install/update software on Ubuntu/Debian.
- apt → newer, user-friendly → best for manual use.
- apt-get → older, stable → best for scripts & Docker.

## Explanation of commands used in Dockerfile:
1. apt install awscli -y - It installs the AWS CLI tool for interacting with AWS services
2. apt-get update - It updates the package lists for upgrades and new package installations.

## EC2 Instance Setup Steps:
1. Launch an EC2 instance with Ubuntu.
2. SSH into the instance.
3. Update package lists: sudo apt-get update, sudo apt-get upgrade -y
4. Install Docker: 
    - curl -fsSL https://get.docker.com -o get-docker.sh # download Docker installation script
    - sudo sh get-docker.sh # run the script to install Docker
    - sudo usermod -aG docker ubuntu # add ubuntu user to docker group
    - newgrp docker # apply new group membership