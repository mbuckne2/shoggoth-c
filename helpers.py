import os
import pandas as pd

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


#TODO: there is now size, line, and file of each malloc and free
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
        return [0, 0, [], []]

    mallocs = df[df['Type'].isin(['MALLOC', 'CALLOC'])]
    frees = df[df['Type'] == 'FREE']

    # check for address parity
    # Filter the DataFrame to get MALLOC and FREE addresses separately
    malloc_addresses = df[df['Type'] == 'MALLOC']['Address']
    free_addresses = df[df['Type'] == 'FREE']['Address']

    # Check if MALLOC addresses all match FREE addresses
    mallocs_without_frees = malloc_addresses[~malloc_addresses['Address'].isin(free_addresses['Address'])]
    frees_without_mallocs = free_addresses[~free_addresses['Address'].isin(malloc_addresses['Address'])]

    return mallocs.shape[0], frees.shape[0], mallocs_without_frees, frees_without_mallocs, df
