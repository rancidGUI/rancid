import os


def check_file_access(path):
    if not os.access(path, os.F_OK):
        return False, 'File is not found'
    elif not os.access(path, os.R_OK):
        return False, 'File is not readable'
    elif not os.access(path, os.W_OK):
        return False, 'File is not writable'
    else:
        return True, ''


def check_json_key(json, *args):

    for arg in args:
        if arg not in json:
            return False, arg
    return True, ''

