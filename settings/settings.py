import ConfigParser
from reader_writer.reader import read_file
from reader_writer.writer import write_file
from rancid_conf.rancid_conf import set_value

def get_setting(param):
    i = 0
    arr = []
    config = ConfigParser.ConfigParser(allow_no_value = True)
    config.read(param)
    sections = config.sections()
    for i in range(len(sections)):
        arr.append(dict(config.items(sections[i])))
    return arr

def set_settings(content,param):
    if param['cloginrc_file_path'] == "" or param['cloginrc_file_path'] is None:
        content1 = set_value(content,'CLOGINRC_FILE_PATH',None)
    else:
        content1 = set_value(content,'CLOGINRC_FILE_PATH',param['cloginrc_file_path'])

    if param['rancid_conf_path'] == "" or param['rancid_conf_path'] is None:
        content2 = set_value(content1,'RANCID_CONF_PATH',None)
    else:
        content2 = set_value(content1,'RANCID_CONF_PATH',param['rancid_conf_path'])

    if param['router_db_dir'] == "" or param['router_db_dir'] is None:
        content3 = set_value(content2,'ROUTER_DB_DIR',None)
    else:
        content3 = set_value(content2,'ROUTER_DB_DIR',param['router_db_dir'])

    if param['tftp_url'] == "" or param['tftp_url'] is None:
        content4 = set_value(content3,'TFTP_URL',None)
    else:
        content4 = set_value(content3,'TFTP_URL',param['tftp_url'])
    return content4
