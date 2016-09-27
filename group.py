from rancid_conf import rancid_conf
from flask import jsonify, request
from flask.views import MethodView
from reader_writer.reader import read_file
from reader_writer.writer import write_file
from router_db.router_db import count_device
import pprint



CONFIG_FILE_PATH = rancid_conf.get_value(read_file("./conf.ini"),"RANCID_CONF_PATH")
ROUTER_FILE_PREFIX = rancid_conf.get_value(read_file("./conf.ini"),"ROUTER_DB_DIR")
class Groups(MethodView):

    def get(self):
        try:
            groups = []
            content = read_file(CONFIG_FILE_PATH)
            list_of_groups = rancid_conf.get_value(content, "LIST_OF_GROUPS")
            list_of_groups_split = list_of_groups.split()
            for i in range(len(list_of_groups_split)):
                groups.append(count_device(read_file(ROUTER_FILE_PREFIX + list_of_groups_split[i] + '/router.db'),list_of_groups_split[i]))
            return jsonify(groups=groups), 200
        except IOError as e:
            return jsonify(message=str(e)), 500

    def post(self):
        data = request.get_json()
        if 'group_name' not in data:
            return jsonify(message="Missing key 'group_name'"), 400
        if rancid_conf.check_value(data['group_name']) == 1:
            return jsonify(message="BAD FORMAT 'group_name'"), 400
        try:
            content = read_file(CONFIG_FILE_PATH)
            LIST_OF_GROUPS = rancid_conf.get_value(content, "LIST_OF_GROUPS")
            if rancid_conf.if_exist(data['group_name'], LIST_OF_GROUPS) == 1:
                return jsonify(message="'group_name' already exist"), 400
            new_content = rancid_conf.set_value(content, "LIST_OF_GROUPS", rancid_conf.add_group(LIST_OF_GROUPS, data["group_name"]))
            write_file(CONFIG_FILE_PATH, new_content)
            groups = rancid_conf.get_value(new_content, "LIST_OF_GROUPS")
            rancid_conf.excecute_cmd("/opt/rancid/bin/rancid-cvs")
            return jsonify(groups=groups), 200
        except IOError as e:
            return jsonify(message=str(e)), 500

    def delete(self):
        data = request.get_json()
        if 'group_name' not in data:
            return jsonify(message="Missing key 'group_name'"), 400
        try:
            content = read_file(CONFIG_FILE_PATH)
            new_content = rancid_conf.set_value(content, "LIST_OF_GROUPS", rancid_conf.remove_group(rancid_conf.get_value(content, "LIST_OF_GROUPS"), data["group_name"]))
            write_file(CONFIG_FILE_PATH, new_content)
            groups = rancid_conf.get_value(new_content, "LIST_OF_GROUPS")

            basedir = rancid_conf.get_value(content,"BASEDIR")
            path_groups = basedir+"/"+data["group_name"]
            logdir = basedir+"/logs/"+data["group_name"]
#            cvsroot = basedir+"/SVN/"+data["group_name"] #gerer le cas CVS ou SVN ou GIT ajout de variable
            rancid_conf.excecute_cmd("./sup.sh "+logdir+"  "+path_groups+" ")

            return jsonify(groups=groups), 200
        except IOError as e:
            return jsonify(message=str(e)), 500
