import os
import numpy as np
import pandas as pd
import sys
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_ob_file_path = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = ['wheelbase', 'carlength', 'carwidth', 'carheight', 'curbweight', 'enginesize', 'boreratio', 'stroke', 'compressionratio', 'horsepower', 'peakrpm', 'citympg', 'highwaympg']
            categorical_columns = ['fueltype', 'aspiration', 'doornumber', 'carbody', 'drivewheel', 'enginelocation', 'enginetype', 'cylindernumber', 'fuelsystem', 'company']

            num_pipeline = Pipeline(
                steps= [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline(
                steps= [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder(handle_unknown='ignore')),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorical Columns: {categorical_columns}")
            logging.info(f"Numerical Columns: {numerical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train and test data completed")

            logging.info("Obtaining pre-processing object")
            preprocessing_obj = self.get_data_transformer_object()
            target_column_name = 'price'

            # Performing pre-processing activities
            logging.info("Removing unwanted columns from the dataset and creating compnay column")
            train_df['company'] = train_df['CarName'].apply(lambda x: x.split(' ')[0])
            test_df['company'] = test_df['CarName'].apply(lambda x: x.split(' ')[0])

            train_df.drop(columns=['car_ID', 'CarName', 'symboling'], inplace=True)
            test_df.drop(columns=['car_ID', 'CarName', 'symboling'], inplace=True)

            train_df['company'].replace("vw", "volkswagen", inplace=True)
            train_df['company'].replace("maxda", "mazda", inplace=True)
            train_df['company'].replace("toyouta", "toyota", inplace=True)
            train_df['company'].replace("vokswagen", "volkswagen", inplace=True)
            train_df['company'].replace("porcshce", "porsche", inplace=True)
            train_df['company'].replace("Nissan", 'nissan', inplace=True)

            test_df['company'].replace("vw", "volkswagen", inplace=True)
            test_df['company'].replace("maxda", "mazda", inplace=True)
            test_df['company'].replace("toyouta", "toyota", inplace=True)
            test_df['company'].replace("vokswagen", "volkswagen", inplace=True)
            test_df['company'].replace("porcshce", "porsche", inplace=True)
            test_df['company'].replace("Nissan", 'nissan', inplace=True)

            # Creating the input train and test features
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saved pre-processing object")

            save_object(
                file_path = self.data_transformation_config.preprocessor_ob_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_ob_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)