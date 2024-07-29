import os
import sys
import logging

# Define the logging format string
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Define the directory where logs will be stored
log_dir = "logs"

# Define the path to the log file
log_filepath = os.path.join(log_dir, "running_logs.log")

# Create the log directory if it does not exist
os.makedirs(log_dir, exist_ok=True)

# Configure the logging settings
logging.basicConfig(
    level=logging.INFO,          # Set the logging level to INFO
    format=logging_str,          # Set the logging format

    # Define the handlers for logging
    handlers=[
        logging.FileHandler(log_filepath),  # Log to a file
        logging.StreamHandler(sys.stdout)   # Log to the console (stdout)
    ]
)

# Create a logger with the name "PDD"
logger = logging.getLogger("PDD")
