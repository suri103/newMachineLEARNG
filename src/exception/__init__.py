import os,sys

class CustomException(Exception):
    def __init__(self,error_massage:Exception,error_details:sys):
        self.error_massage = CustomException.get_detailed_error_massage(error_massage=error_massage,error_details=error_details)
        


    @staticmethod
    def get_detailed_error_massage(error_massage:Exception,error_details:sys)->str:
        _,_, exce_tb= error_details.exc_info()
        exception_block_linenumber= exce_tb.tb_frame.f_lineno
        try_block_line_number = exce_tb.tb_lineno
        file_name = exce_tb.tb_frame.f_code.co_filename

        error_massage = f"""
        Error occured in the execution of:
        [{file_name}] at 
        try block line number : [{try_block_line_number}]
        and exception block line number :[{exception_block_linenumber}]
        error massage : [{error_massage}]
        """
        return error_massage
    
    def __str__(self) :
        return self.error_massage
    def __repr__(self) :
        return CustomException.__name__.str()