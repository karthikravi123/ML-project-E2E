
##feature ENgineering ,Data cleaning
import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer  ##to create a pipeline
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj

@dataclass
class DataTransformationConfig:
    preprocesor_obj_file = os.path.join('artifacts',"preprocesspr.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):

        """
        This function is resposnible for data transformation 
        """

        try:
            numerical_columns = ['reading_score', 'writing_score'] 
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
        
            num_pipeline = Pipeline(
            steps=[
                ##mputer responsible to handle missing value
                ("imputer",SimpleImputer(strategy='median')),
                ("scaler",StandardScaler())
                ]
                )
            
            cat_pipeline = Pipeline(
                steps=[ 
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                    
                ]
            )
            logging.info("Numeric column standard scaling completed")
            logging.info("categorical columns encoding completed")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                    ]
            )
            logging.info(f"Categorical columns:{categorical_columns}")
            logging.info(f"Numerical columns : {numerical_columns}")

            return preprocessor
    
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):

        try:
            
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()
            target_columns = "math_score"
            numeric_columns = ['reading_score', 'writing_score'] 

            input_feature_train_df= train_df.drop(columns=[target_columns],axis=1)
            target_feature_train_df = train_df[target_columns]

            input_feature_test_df= test_df.drop(columns=[target_columns],axis=1)
            target_feature_test_df = test_df[target_columns]

            logging.info(
                f"applying preprocesing object on training dataframe and testing dataframe"
            )

            input_feature_train_arr= preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr= preprocessing_obj.fit_transform(input_feature_test_df)


            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
                ]

            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)] 


            logging.info(
                f"saved preprocessing object"
            )
            
            ##save the picklefile
            save_obj(
            file_path = self.data_transformation_config.preprocesor_obj_file,
            obj = preprocessing_obj
                )


            return (
                train_arr,test_arr,self.data_transformation_config.preprocesor_obj_file,

            )
        
   
        except Exception as e:
            raise CustomException(e,sys)