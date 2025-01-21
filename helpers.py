import math
import os
import random

import timeout_decorator

source_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(source_dir)
submission_dir = os.path.join(parent_dir, "submission") # os.path.join(source_dir, 'source_code')#

logger_exec_path =  submission_dir + '/StudentProgramLogger'
file_load_path =    submission_dir + '/StudentProgramBase'


def call_or_timeout(function):
    try:
        return function()
    except timeout_decorator.TimeoutError:
        return [False, False, False], ["Function took too long and was timed out.", "Function took too long and was timed out.", "Function took too long and was timed out."]
    except TimeoutError:
        return [False, False, False], ["Function took too long and was timed out.",
                                       "Function took too long and was timed out.",
                                       "Function took too long and was timed out."]
    except Exception as e:
        return [False, False, False], [f"Uncaught Exception in autograder: {e}",
                                       f"Uncaught Exception in autograder: {e}",
                                       f"Uncaught Exception in autograder: {e}"]


def error_handling(error):
    if error == -11:
        return "Your program encountered a segmentation fault."
    else:
        return "Your program encountered an error. Exit code: " + str(error)


def remove_file(file_name):
    try:
        os.remove(file_name)
    except:
        pass
