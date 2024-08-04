# # Basic Import
# import numpy as np
# import pandas as pd

# # Modelling
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
# from catboost import CatBoostClassifier
# from xgboost import XGBClassifier
# import warnings
# import os

# from urllib.parse import urlparse
# import dagshub
# import mlflow
# import mlflow.sklearn

# from src.PDD import logger
# from src.PDD.utils.common import save_object, evaluate_model
# from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

# from dataclasses import dataclass



# @dataclass
# class ModelTrainerConfig:
#     trained_model_file_path = os.path.join("artifacts","model.pkl")

# class ModelTrainer:
#     def __init__(self):
#         self.model_trainer_config = ModelTrainerConfig()

#     # FOR LOGGING INTO MLFLOW
#     def eval_metrics(self, true, pred):
#         f1score = f1_score(true, pred, average='weighted')
#         accuracy = accuracy_score(true, pred)
#         return f1score, accuracy

#     def initiate_model_trainer(self,train_array,test_array):
#         try:
#             logger.info("Split training and test input data")
#             X_train,y_train,X_test,y_test=(
#                 train_array[:,:-1],
#                 train_array[:,-1],
#                 test_array[:,:-1],
#                 test_array[:,-1]
#             )
            
#             models = {
#                 "Decision Tree Classifier": DecisionTreeClassifier(random_state=42),
#                 "Random Forest Classifier": RandomForestClassifier(random_state=42),
#                 "XGBClassifier": XGBClassifier(random_state=42),
#                 "CatBoost Classifier": CatBoostClassifier(verbose=False, random_state=42),
#                 "Gradient Boosting Classifier": GradientBoostingClassifier(random_state=42)
#             }

#             model_report:dict = evaluate_model(X_train,y_train,X_test,y_test,models)

#             ## To get best model score from dict
#             best_model_score = max(sorted(model_report.values()))

#              ## To get best model name from dict

#             best_model_name = list(model_report.keys())[
#                 list(model_report.values()).index(best_model_score)
#             ]
#             best_model = models[best_model_name]
#             print(f"Best model:{best_model_name}")


#             #MLFLOW

#             mlflow.set_registry_uri("https://dagshub.com/paridhi3/Phishing-Domain-Detection.mlflow")
#             tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
#             dagshub.init(repo_owner='paridhi3', repo_name='Phishing-Domain-Detection', mlflow=True)

#             with mlflow.start_run():

#                 y_test_pred = best_model.predict(X_test)

#                 (f1score, accuracy) = self.eval_metrics(y_test, y_test_pred)

#                 mlflow.log_metric("f1-score", f1score)
#                 mlflow.log_metric("accuracy", accuracy)

#                 # Model registry does not work with file store
#                 if tracking_url_type_store != "file":

#                     # Register the model
#                     # There are other ways to use the Model Registry, which depends on the use case,
#                     # please refer to the doc for more information:
#                     # https://mlflow.org/docs/latest/model-registry.html#api-workflow
#                     mlflow.sklearn.log_model(best_model, "model", registered_model_name = best_model)

#                 else:
#                     mlflow.sklearn.log_model(best_model, "model")


#             if best_model_score<0.6:
#                 raise Exception("No best model found")
            
#             logger.info(f"Best model found!")

#             save_object(
#                 file_path=self.model_trainer_config.trained_model_file_path,
#                 obj=best_model
#             )

#             predicted_values = best_model.predict(X_test)

#             accuracy = accuracy_score(y_test, predicted_values)
#             return accuracy


#         except Exception as e:
#             raise e

# Basic Import
import numpy as np
import pandas as pd

# Modelling
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
import warnings
import os

from urllib.parse import urlparse
import dagshub
import mlflow
import mlflow.sklearn

from src.PDD import logger
from src.PDD.utils.common import save_object, evaluate_model
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

from dataclasses import dataclass



@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    # FOR LOGGING INTO MLFLOW
    def eval_metrics(self, true, pred):
        f1score = f1_score(true, pred, average='weighted')
        accuracy = accuracy_score(true, pred)
        return f1score, accuracy

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logger.info("Split training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            models = {
                "Random Forest Classifier": RandomForestClassifier(random_state=42),
                "Decision Tree Classifier": DecisionTreeClassifier(random_state=42),
                "XGBClassifier": XGBClassifier(random_state=42),
                "CatBoost Classifier": CatBoostClassifier(verbose=False, random_state=42),
                "Gradient Boosting Classifier": GradientBoostingClassifier(random_state=42)
            }

            model_report:dict = evaluate_model(X_train, y_train, X_test, y_test, models)

            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

             ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            print(f"Best model: {best_model_name}")








            #MLFLOW

            mlflow.set_registry_uri("https://dagshub.com/paridhi3/Phishing-Domain-Detection.mlflow")
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            dagshub.init(repo_owner='paridhi3', repo_name='Phishing-Domain-Detection', mlflow=True)

            with mlflow.start_run():

                y_test_pred = best_model.predict(X_test)

                (f1score, accuracy) = self.eval_metrics(y_test, y_test_pred)

                mlflow.log_metric("f1-score", f1score)
                mlflow.log_metric("accuracy", accuracy)

                # Model registry does not work with file store
                if tracking_url_type_store != "file":

                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.sklearn.log_model(best_model, "model", registered_model_name = best_model)

                else:
                    mlflow.sklearn.log_model(best_model, "model")










            if best_model_score<0.6:
                raise Exception("No best model found")
            
            logger.info(f"Best model found!")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted_values = best_model.predict(X_test)

            accuracy = accuracy_score(y_test, predicted_values)
            return accuracy


        except Exception as e:
            raise e