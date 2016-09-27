import csv
import re

# Ajoute une nouvelle machine directement dans le fichier 'file_path'
def add_machine(file_path, ip, type_machine, status):
    with open(file_path, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', lineterminator='\n', skipinitialspace=True)
        writer.writerow([ip, type_machine, status])


# Retourne l'index d'une machine, -1 si elle n'est pas trouvee
def get_machine_index(machines, ip_machine):
    for index in range(len(machines)):
        if ip_machine in machines[index]:
            return index
    return -1


# Supprime une machine
def remove_machine(machines, index):
    del machines[index]
    return machines


# Modifie le status d'une machine
def update_status(machines, ip_machine, new_status):
    for index in range(len(machines)):
        if ip_machine in machines[index]:
            machines[index][2] = new_status
            break

    return machines


# Modifie le type d'une machine
def update_type(machines, ip_machine, new_type):
    for index in range(len(machines)):
        if ip_machine in machines[index]:
            machines[index][1] = new_type
            break

    return machines


# Modifie l'ip d'une machine
def update_machine(machines, ip_machine, new_machine):
    for index in range(len(machines)):
        if ip_machine in machines[index]:
            machines[index][0] = new_machine
            break

    return machines


# Appel la bonne methode d'update en fonction du 'param'
def update(param, machines, ip_machine, new_value):
    if param == 'machine':
        return True, update_machine(machines, ip_machine, new_value)
    elif param == 'type':
        return True, update_type(machines, ip_machine, new_value)
    elif param == 'status':
        return True, update_status(machines, ip_machine, new_value)
    else:
        return False, machines

# retourne le nombre de Device Up and Down et total d'un group_name
def count_device(content, group_name):
    r = {}
    r['group_name'] = group_name
    r['up'] = 0
    r['down'] = 0
    r['total'] = 0
    regexup = r"""^(.*;up)$"""
    regexdown = r"""^(.*;down)$"""
    lines = content.split('\n')
    matchedLines = []
    for line in lines:
        up = re.match(regexup,line,flags=re.IGNORECASE)
        down = re.match(regexdown,line,flags=re.IGNORECASE)
        if up:
            r['up'] += 1
        if down:
            r['down'] += 1
    r['total'] = r['up'] + r['down']
    return r
