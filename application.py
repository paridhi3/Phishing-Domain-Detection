from src.PDD import logger
from src.PDD.components.data_ingestion import DataIngestion

if __name__ == "__main__":
    logger.info("Execution has started")

    try:
        data_ingestion = DataIngestion()
        data_ingestion.initiate_data_ingestion()

    except Exception as e:
        raise e