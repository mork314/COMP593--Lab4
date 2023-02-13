import re
import sys
import os
from sys import argv

#One parameter - path
def get_log_file_path_from_cmd_line(param_num):
    """Gets the full path of a log file from the command line - exits if 
    there aren't enough parameters or if the parameter specified is not
    a valid file path.

    Args:
        param_num (int): Parameter number of the desired path

    Returns:
        str: Full path of the log file
    """
    num_params = len(sys.argv) - 1
    if num_params >= param_num:
        path = argv[param_num]
        if os.path.isfile(path):
            return os.path.abspath(path)
        else:
            print("ERROR: No valid file path found")
            sys.exit()
    else:
        print("ERROR: No command line parameter found")
        sys.exit()

def filter_log_by_regex(log_file, regex, ignore_case=True, print_summary=False, print_records=False):
    """Searches a file line by line for a regex, returns matching lines + capture groups

    Args:
        log_file (_type_): _description_
        regex (_type_): _description_
        ignore_case (bool, optional): _description_. Defaults to True.
        print_summary (bool, optional): _description_. Defaults to False.
        print_records (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    open_file = open(log_file)
    record_list = []
    match_list = []
    match_count = 0
    case_ignoring = ''
    if ignore_case == True:
        case_ignoring = 'case-insensitive'
    elif ignore_case == False:
        case_ignoring = 'case-sensitive'
    for line in open_file:
        if ignore_case == True:
            result = re.search(regex, line, re.IGNORECASE)
        else:
            result = re.search(regex, line, re.IGNORECASE)
        if result:
            record_list.append(line)
            match_count += 1
            if result.lastindex:
                match_list.append(result.groups())
    
    if print_records == True:
        for item in record_list:
            print(item)
    if print_summary == True:
        print(f"{match_count} records matched the regex '{regex}', and {case_ignoring} regex matching was performed")
    return record_list, match_list