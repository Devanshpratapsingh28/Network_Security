import os
import sys
import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.constant.training_pipeline import TARGET_COLUMN,SAVED_MODEL_DIR
from networksecurity.utils.main_utils.utils import evaluate_models,save_object,load_object
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import mlflow
from mlflow.models import infer_signature
import dagshub


dagshub.init(repo_owner='devanshprataps6', repo_name='Network_Security', mlflow=True)


class ModelTrainer:

    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,best_model,classification_metrics,X=None):
        try:
            with mlflow.start_run():
                mlflow.log_metric("f1_score", classification_metrics.f1_score)
                mlflow.log_metric("precision", classification_metrics.precision_score)
                mlflow.log_metric("recall_score", classification_metrics.recall_score)

                # # Model Logging with sign
                # y_pred = best_model.predict(X)
                # sign = None
                # if X is not None:
                #     sign = infer_signature(X,y_pred)
                # mlflow.sklearn.log_model(
                #     sk_model=best_model,
                #     name="model",
                #     signature=sign,
                #     input_example=X[0:2] if X is not None else None
                # )
                # logging.info("Model logged successfully in MLflow")
        except Exception as e:
            logging.warning(f"MLflow tracking failed: {e}. Continuing without tracking.")

    def train_model(self,X_train,y_train,x_test,y_test):
        models = {
            "Support Vector Classifier": SVC(),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier()
        }

        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                'splitter':['best','random'],
                'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                'n_estimators': [50, 200, 250],
                'max_features': ['sqrt', 'log2'],
                'max_depth': [10, 20, 50, None],
                'min_samples_split': [2, 5, 7, 10],
                'min_samples_leaf': [1, 2, 4, 8],
                'bootstrap': [True, False]
            },
            "Support Vector Classifier": {
                'kernel': ['linear', 'rbf'],
                'C': [0.1, 0.5, 1, 10],  
                'gamma': ['scale', 0.5, 0.1],
                'class_weight': [None, 'balanced']
            }
        }

        model_report,best_estimators = evaluate_models(
            X_train, y_train, x_test, y_test, models, params
        )
        
        ## Best model
        best_model_name = max(model_report, key=model_report.get)
        best_model = best_estimators[best_model_name]

        ## Training score
        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(
            y_true=y_train,y_pred=y_train_pred
        )  

        # self.track_mlflow(best_model,classification_train_metric,X_train)

        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(
            y_true=y_test,y_pred=y_test_pred
        )
        self.track_mlflow(best_model,classification_test_metric,x_test)
        
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model = NetworkModel(
            model=best_model
        )
        save_object(self.model_trainer_config.trained_model_file_path, obj=Network_Model)
        
        # Save raw model to SAVED_MODEL_DIR
        os.makedirs(SAVED_MODEL_DIR, exist_ok=True)
        model_path = os.path.join(SAVED_MODEL_DIR, "model.pkl")
        save_object(model_path, obj=best_model)
        
        
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact


    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            x_train = train_df.drop(columns=[TARGET_COLUMN]).values
            y_train = train_df[TARGET_COLUMN].values

            x_test = test_df.drop(columns=[TARGET_COLUMN]).values
            y_test = test_df[TARGET_COLUMN].values

            model_trainer_artifact = self.train_model(
                x_train,y_train,x_test,y_test
            )
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
