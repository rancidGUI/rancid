import re
import subprocess

# Recupere la valeur de la 'key' correspondante
def get_value(content, key):
    lines = content.split('\n')
    regex = r"""^(%s)=['"]?([^'";]+)+['"]?([^"]*)$""" % key

    for line in lines:
        match = re.search(regex, line)
        if match:
            return match.group(2)
    return ""


# Assigne la 'value' a la 'key' correspondante
def set_value(content, key, value):
    lines = content.split('\n')
    regex = r"""^(?P<key>%s)=(?P<quote_beg>['"]?)([^'";]+)+(?P<quote_end>['"]?)(?P<string_end>[^"]*)$""" % key

    for index in range(len(lines)):
        lines[index] = re.sub(regex, r'\g<key>=\g<quote_beg>%s\g<quote_end>\g<string_end>' % value, lines[index])

    return '\n'.join(lines)


# Ajoute un groupe
def add_group(raw_group, item):
    groups = raw_group.split(' ')
    groups.append(item)

    return ' '.join(groups)


# Supprime un groupe
def remove_group(raw_group, item):
    groups = raw_group.split(' ')
    groups.remove(item)

    return ' '.join(groups)


# Modifie un groupe
def update_group(raw_group, old_value, new_value):
    groups = raw_group.split(' ')
    try:
        idx = groups.index(old_value)
        groups[idx] = new_value
    except ValueError:
        return raw_group

    return ' '.join(groups)

# execute une commande
def excecute_cmd(cmd):
    try:
        subprocess.call(cmd, shell=True)
    except IOError as e:
        return jsonify(message=str(e)), 500

#check_value
def check_value(name):
    regex =r"""^[-_a-zA-Z0-9.]+$"""
    match = re.search(regex, name)
    if match:
        return 0
    return 1

def if_exist(name, content):
    lines = content.split(' ')
    matchedLines = []
    for line in lines:
        if name == line:
            matchedLines.append(line)
    if len(matchedLines) > 0:
        return 1
    else:
        return 0
