import os
import pandas as pd

import timeout_decorator

source_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(source_dir)
submission_dir = os.path.join(parent_dir, "submission") # os.path.join(source_dir, 'source_code')#
results_dir = os.path.join(parent_dir, "results")  # os.path.join(source_dir, 'source_code')#

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


def find_and_remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        return True
    else:
        return False


# TODO: there is now size, line, and file of each malloc and free
# will be useful for generating student feedback

# returns malloc data
#
# num mallocs
# num frees
# [mallocs without frees]
# [frees without mallocs]
# dataframe
#
def test_mallocs():
    column_names = ['Type', 'Address', 'Size', 'Line', 'File']
    try:
        df = pd.read_csv("malloc_log.csv", header=None, names=column_names)
    except:
        return 0, 0, None, None, None

    mallocs = df[df['Type'].isin(['MALLOC', 'CALLOC'])]
    frees = df[df['Type'] == 'FREE']

    # Check if MALLOC addresses all match FREE addresses
    mallocs_without_frees = mallocs[~mallocs['Address'].isin(frees['Address'])]
    frees_without_mallocs = frees[~frees['Address'].isin(mallocs['Address'])]

    return mallocs.shape[0], frees.shape[0], mallocs_without_frees, frees_without_mallocs, df
