from flask import jsonify, request, abort
from flask.views import MethodView
from reader_writer.writer import write_file
from router_db import router_db
from utils import check_file_access, check_json_key
from rancid_conf.rancid_conf import get_value
from reader_writer.reader import read_file
from rancid_conf import rancid_conf
from versionning.svn import get_list_version
from versionning.svn import svn_cat
from versionning.svn import svn_diff

ROUTER_FILE_PREFIX = get_value(read_file("./conf.ini"),"ROUTER_DB_DIR")

class Versionning(MethodView):

    def get(self, param, param2, param3):

        path = ROUTER_FILE_PREFIX + param + '/configs/'+param2
        b, msg = check_file_access(path)
        if not b:
            return jsonify(message=msg), 400

        try:
            tab_param = {"full" : " ", "None" : " -l 5 "}
            rancid_conf.excecute_cmd("mkdir ./tmp")
            dir_temp = "./tmp/"+param2+"version.txt"
            if param3.isnumeric() is True:
                version = svn_cat(param,param2,param3)
                rancid_conf.excecute_cmd("rm -fr ./tmp")
                return jsonify(version=version), 200
            elif param3.find("diff") > -1:
                diff = svn_diff(param,param2,param3[4:])
                rancid_conf.excecute_cmd("rm -fr ./tmp")
                return jsonify(verisons_diff=diff), 200
            else:
                rancid_conf.excecute_cmd("svn log"+tab_param[param3]+path+" > "+dir_temp)
                list_of_version = get_list_version(read_file(dir_temp))
                rancid_conf.excecute_cmd("rm -fr ./tmp")
                return jsonify(versions=list_of_version), 200
        except IOError as e:
            return jsonify(message=str(e)), 500
