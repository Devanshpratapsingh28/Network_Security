import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info() # (type, value, traceback)
        
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename
        self.fun_name = exc_tb.tb_frame.f_code.co_name
    
    def __str__(self):
        return f"Error occured in python file name {self.file_name} at line number {self.lineno} having error message {str(self.error_message)}."
        