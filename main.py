from src.PDD import logger
from src.PDD.components.s01_data_ingestion import DataIngestion
from src.PDD.components.s02_data_transformation import DataTransformation
from src.PDD.components.s03_model_training import ModelTrainer

from src.PDD.pipeline.prediction_pipeline import CustomData, PredictPipeline

if __name__ == "__main__":
    logger.info("Execution has started")

    try:
        data_ingestion = DataIngestion()
        train_data_path, test_data_path, raw_data_path = data_ingestion.initiate_data_ingestion()

        data_transformation = DataTransformation()
        train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data_path, test_data_path, raw_data_path)

        model_trainer = ModelTrainer()
        print(model_trainer.initiate_model_trainer(train_arr, test_arr))

        URL = "https://github.com/krishnaik06/mlproject/blob/main/app.py"
        custom_data = CustomData.from_url(URL)
        features_df = custom_data.get_data_as_data_frame()
        print(features_df)

        print("Predicting...")
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(features_df)
        print(results)



    except Exception as e:
        raise e