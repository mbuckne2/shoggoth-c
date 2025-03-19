import os
import subprocess
import time

import pandas as pd

import timeout_decorator

# Get the current directory of the Python script (source directory)
source_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the parent directory of the source directory
parent_dir = os.path.dirname(source_dir)

submission_dir = os.path.join(parent_dir, "submission") # os.path.join(source_dir, 'source_code')#
results_dir = os.path.join(parent_dir, "results")  # os.path.join(source_dir, 'source_code')#

logger_exec_path =  submission_dir + '/StudentProgramLogger'
main_exec_path =    submission_dir + '/StudentProgramBase'


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


def describe_error(error):
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
    """
    Parses the malloc log file and returns stats about it, plus a dataframe with its full contents
    :return:
    num mallocs
    num frees
    [mallocs without frees]
    [frees without mallocs]
    dataframe
    """
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


def execute_program(program_args, runtime_input, file_path=main_exec_path):
    """
    :param program_args: arguments to execute the program with, should be an array of strings.
        Each one is an argument piece. ex: ['-i', 'fileName.bmp']
    :param runtime_input: array of strings representing inputs to write to the stdin during program execution.
        No newline chars needed
    :param file_path: file path of the program, defaults to standard, but you can also use logger or a custom variant
    :return: program stdout output and error status

    Sample Usage: output, return_code = helpers.execute_program(['-i' 'fileName.bmp'], [], file_path=helpers.main_exec_path)

    NOTE: All file pathing is based upon the root directory of the python program, not the submissions folder where the code is!
    """

    command = [file_path] + program_args

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    start_time = time.time()
    while True:
        if process.poll() is not None:  # If process is done
            break
        if time.time() - start_time > 5:  # 10-second timeout
            process.terminate()
            raise TimeoutError("The process took too long and was terminated.")

        try:
            for line in runtime_input:
                process.stdin.write(str(line) + '\n')
            process.stdin.flush()  # Make sure to flush the buffer
        except BrokenPipeError:
            # This exception occurs when the process has already terminated and no longer accepts input.
            break

    stdout, stderr = process.communicate()
    process.wait()

    return stdout, process.returncode
