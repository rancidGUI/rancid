import re
import types
from reader_writer.reader import read_file

# recupere directives
def get_value(content, machine):
    lines = content.split('\n')
    regex = r"""^(?P<Command>add [^\s]+)\s+(?P<Device>%s)\s+(?P<Attributs>{.+})\s?#?(?P<Comments>.+)?$""" % machine
    matchedLines = []
    for line in lines:
        matchs = re.match(regex,line)
        if matchs:
            matchedLines.append(matchs.groupdict())
    return matchedLines

# Ajoute directives
def add_value(file_path, directives):
    with open(file_path, 'a') as f:
        if isinstance(directives, list):
            for e in directives:
                f.write(e+'\n')
        else:
            f.write(directives+'\n')

# supprimer directives
def remove_value(file_path, directives):
     content = read_file(file_path)
     lines = content.split('\n')
     with open(file_path, 'w+') as new_file:
         for line in lines:
            if directives == line:
                None
            else:
                new_file.write(line+'\n')

# check_value
def check_value(file_path, directives):
    content = read_file(file_path)
    lines = content.split('\n')
    matchedLines = []
    for line in lines:
        if directives == line:
            matchedLines.append(line)
    if len(matchedLines) > 0:
        return 1
    else:
        return 0
