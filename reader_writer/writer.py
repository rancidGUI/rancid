

# Ecrit le 'content' dans le fichier 'file_path'
def write_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content+'\n')
