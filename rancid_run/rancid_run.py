import subprocess
from rancid_conf.rancid_conf import excecute_cmd
from crontab import CronTab
from rancid_conf import rancid_conf
from reader_writer.reader import read_file
import re
user = 'rancid'
TFTP_URL = rancid_conf.get_value(read_file("./conf.ini"),"TFTP_URL")
def get_cronjob(param):
    tab = CronTab(user=user)
    result = []
    cron_lines = []
    if param == 'full':
        regex =r"""^(?P<MIN>[\d\*-,]*) (?P<HOUR>[\d\*-,]*) (?P<MONTH>[\d\*-,]*) (?P<DAY>[A-Z\d\*-,]*) (?P<DOWEEK>[A-Z\d\*-,]*) (?P<Commands>[^#]*)\s?#?(?P<Comments>.+)?$"""
        content = tab.render()
        cron_lines = content.split('\n')
    else:
        regex =r"""^(?P<MIN>[\d\*-,]*) (?P<HOUR>[\d\*-,]*) (?P<MONTH>[\d\*-,]*) (?P<DAY>[A-Z\d\*-,]*) (?P<DOWEEK>[A-Z\d\*-,]*) (?P<Commands>[^#]*%s)\s+?#?(?P<Comments>.+)?$""" % param
        lines = tab.find_command(param)
        for l in lines:
            cron_lines.append(l.render())
    for line in cron_lines:
        match = re.match(regex, line)
        if match:
            result.append(match.groupdict())
    return result

def add_cronjob(data):
    if data['cron_job'][0]['Type'] == "tftp":
        tftp(data)
    else:
        tab_param = {"group" : "", "device" : " -r"}
        cmd ="rancid-run"+tab_param[data['cron_job'][0]['Type']]+" "+data['cron_job'][0]['Name']
        if len(get_cronjob(data['cron_job'][0]['Name'])) > 0:
            return "Job already created"
        else:
            if data['cron_job'][0]['Delay'] == "ok":
                tab = CronTab(user=user)
                cron_job = tab.new(command=cmd, comment=data['cron_job'][0]['Comments'])
                cron_job.setall(data['cron_job'][0]['MIN'],
                                data['cron_job'][0]['HOUR'],
                                data['cron_job'][0]['MONTH'],
                                data['cron_job'][0]['DAY'],
                                data['cron_job'][0]['DOWEEK'])
                tab.write()
                return "Job created"
            else:
                excecute_cmd(cmd+" &")
                return "backup Launch"

def create_cronjob(data):
    cmd1 = data['cron_job'][0]['MIN']+" "
    cmd1 += data['cron_job'][0]['HOUR']+" "
    cmd1 += data['cron_job'][0]['MONTH']+" "
    cmd1 += data['cron_job'][0]['DAY']+" "
    cmd1 += data['cron_job'][0]['DOWEEK']+" "+data['cron_job'][0]['Commands']+" # "+data['cron_job'][0]['Comments']
    return cmd1

def delete_cronjob(data):
    tab = CronTab(user=user)
    cmd = data['cron_job'][0]['Commands']
    lines = tab.find_command(cmd)
    cmd1 = create_cronjob(data)
    nb_delete = 0
    for l in lines:
        if cmd1 == l.render():
            tab.remove(l)
            nb_delete += 1
    if nb_delete > 0:
        tab.write()
        return "Job Deleted"
    else:
        return "no job to delete"

def tftp(data):
    tab_param = {"cisco" : "clogin",
     "Catalyst switch" : "clogin",
     "Extreme switch" : "clogin",
     "Juniper ERX/E-series" : "clogin",
     "Procket Networks" : "clogin",
     "Redback router" : "clogin" ,
     "Alteon" : "alogin",
     "Avocent" : "avologin",
     "Bay Networks (nortel)" : "blogin ",
     "ADC-kentrox EZ-T3 mux" : "elogin",
     "Foundry" : "flogin",
     "HP Procurve switches" : "fnlogin",
     "Cisco AGMs" : "hlogin",
     "Hitachi routers" : "htlogin",
     "Juniper Networks" : "jlogin",
     "MRV optical switch" :"mrvlogin",
     "Mikrotik routers" : "mtlogin",
     "Netscreen firewalls" : "nlogin",
     "Netscaler" : "nslogin",
     "Riverstone" : "rivlogin",
     "Netopia" : "tlogin",
     "Cisco WLCs" : "wlogin",
     "Xirrus" : "xilogin"}
    cmd1 = '"copy running-config tftp://'+TFTP_URL+'/'+data['cron_job'][0]['Name']+'; exit " '
    cmd = "/opt/rancid/bin/"+tab_param[data['cron_job'][0]['type_of_machine']]+" -c "+cmd1+data['cron_job'][0]['Device_name']
    excecute_cmd(cmd+" >> ./tftp_log.txt")
    return "ok"
