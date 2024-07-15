import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys): # This function constructs a detailed error message.
    _, _, exc_tb = error_detail.exc_info() # Extracting traceback information
    file_name = exc_tb.tb_frame.f_code.co_filename # file name where the exception occurred
    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message


class CustomException(Exception): # Custom exception class that extends the base Exception class.

    def __init__(self,error_message,error_detail:sys): # Initializes the CustomException instance with an error message and details.
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self): # Returns the error message string when the exception is converted to a string.
        return self.error_message
    
# from src.logger import logging 
# if __name__=="__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         logging.info("Div by 0 error")
#         raise CustomException(e, sys)