import sys
import logging
from datetime import datetime 
import os



# Create log directory (if it doesn’t exist)
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Create a timestamped log file
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)




logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s] %(lineno)s %(name)s -%(levelname)s - %(message)s ",
    level=logging.INFO,

)


#custom exception handling -documents
def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line numer [{1}] error[{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    
    )

    return error_message


class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)
        self.error_messge  = error_message_detail(error_message,error_detail=error_details)

    def __str__(self):
        return self.error_messge
    

# # Main block
# if __name__ == "__main__":
#     try:
#         a = 1 / 0
#     except Exception as e:
#         logging.info("Logging started due to an exception")
#         custom_error = CustomException(e,sys)
#         logging.error(custom_error)
#         raise custom_error