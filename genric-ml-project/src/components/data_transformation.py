"""Transforming data like data encoding, categorical to numerical ect.."""
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_cofig = DataTransformationConfig()
        
    def get_data_transformer_object(self):
        """
        This function is responsible for data tranformation based on different data types
        """
        try:
            numerical_column = ['reading_score', 'writing_score']
            categorical_column = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encode", OneHotEncoder())
                ]
            )

            logging.info(f"Categorical colums: {categorical_column}")
            logging.info(f"Categorical colums: {numerical_column}")
            
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_column),
                    ("cat_pipeline", cat_pipeline, categorical_column)
                ]
            )


            logging.info("Numerical columns standard scaling completed")
            logging.info("Categorical columns encoding completed")

            return preprocessor    
        except Exception as e:
            raise CustomException(e, sys)
        
    def initate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_colum_name = "math_score"

            input_feature_train_df = train_df.drop(columns=[target_colum_name])
            target_feature_train_df = train_df[target_colum_name]

            input_feature_test_df = test_df.drop(columns=[target_colum_name])
            target_feature_test_df = test_df[target_colum_name]

            logging.info(f"Appliying preprocessing object on training datafrane and testing dataframe.")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_cofig.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_cofig.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)
