from cloginrc_conf import cloginrc_conf
from flask import jsonify, request
from flask.views import MethodView
from reader_writer.reader import read_file
from reader_writer.writer import write_file
from rancid_conf.rancid_conf import get_value

CONFIG_FILE_PATH = get_value(read_file("./conf.ini"),"CLOGINRC_FILE_PATH")

class Cloginrc(MethodView):
    def get(self, param):

        try:
            content = read_file(CONFIG_FILE_PATH)
            directives = cloginrc_conf.get_value(content, param)
            return jsonify(directives=directives), 200
        except IOError as e:
            return jsonify(message=str(e)), 500

    def post(self, param):
        data = request.get_json()
        if 'directives' not in data:
            return jsonify(message="Missing key 'directives'"), 400
        if cloginrc_conf.check_value(CONFIG_FILE_PATH, data["directives"]) == 1:
            return jsonify(message="'directives' already exist in the file"), 400
        try:
            cloginrc_conf.add_value(CONFIG_FILE_PATH, data["directives"])
            directive = cloginrc_conf.get_value(read_file(CONFIG_FILE_PATH), param)
            return jsonify(directive=directive), 200
        except IOError as e:
            return jsonify(message=str(e)), 500

    def delete(self, param):
        data = request.get_json()
        if 'directives' not in data:
            return jsonify(message="Missing key 'directive'"), 400
        if cloginrc_conf.check_value(CONFIG_FILE_PATH, data["directives"]) == 0:
            return jsonify(message="'directives' does not exist in the file"), 400
        try:
            cloginrc_conf.remove_value(CONFIG_FILE_PATH, data["directives"])
            directive = cloginrc_conf.get_value(read_file(CONFIG_FILE_PATH), param)
            return jsonify(directive=directive), 200
        except IOError as e:
            return jsonify(message=str(e)), 500
