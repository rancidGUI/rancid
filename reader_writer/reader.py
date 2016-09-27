import csv


# Renvoie le contenu du fichier 'file_path'
def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


# Supprime les espaces au debut et en fin de 'ligne'
def strip_line(line):
    for index in range(len(line)):
        line[index] = line[index].strip()
    return line


# Lit un fichier au format csv
def read_csv_file(file_path):
    arr = []
    with open(file_path, 'r+a') as csvfile:
        csv_content = csv.reader(csvfile, delimiter=';', skipinitialspace=True)
        for r in csv_content:
            if r > len(r):
                r = strip_line(r)
                arr.append(r)
        return arr

def rewrite_out(content):
    arr = []
    all_machines = []
    for line in content:
        for pair in zip(['Name','Type', 'State'], line):
            arr.append(pair)
            a = dict(arr)
        all_machines.append(a)
    return all_machines
