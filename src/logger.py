import logging  # Importing the logging module for logging events
import os  # Importing the os module to interact with the operating system
from datetime import datetime  # Importing datetime to handle date and time

# Generating a log file name based on the current date and time
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Defining the path where log files will be stored
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
# Creating the directory for logs if it doesn't exist
os.makedirs(logs_path, exist_ok=True)

# Defining the full path to the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configuring the logging settings
logging.basicConfig(
    filename = LOG_FILE_PATH,  # The file to write logs to
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # The format of the log messages
    level = logging.INFO,  # The logging level; INFO level will capture all info, warning, error, and critical messages
)

# if __name__=="__main__":
#     logging.info("Logging has started")