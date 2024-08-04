import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from src.PDD.utils.common import save_object
from src.PDD import logger
import os

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
       

    def initiate_data_transformation(self, train_path, test_path, raw_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logger.info("Reading the train and test file")

            target_column_name = "phishing"

            ## divide the train dataset to independent and dependent feature

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1) # X_train_df
            target_feature_train_df = train_df[target_column_name] # y_train_df

            ## divide the test dataset to independent and dependent feature

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1) # X_test_df
            target_feature_test_df = test_df[target_column_name] # y_test_df

            train_arr = np.c_[np.array(input_feature_train_df), np.array(target_feature_train_df)]
            test_arr = np.c_[np.array(input_feature_test_df), np.array(target_feature_test_df)]

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        
        except Exception as e:
            raise e