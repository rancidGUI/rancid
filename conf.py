from flask import jsonify, request
from flask.views import MethodView
from settings import settings
from reader_writer.reader import read_file
from reader_writer.writer import write_file
CONF_INI = "./conf.ini"

class Conf(MethodView):

    def get(self):
        try:
            conf = settings.get_setting(CONF_INI)
            return jsonify(conf=conf), 200
        except IOError as e:
            return jsonify(message=str(e)), 500

    def post(self):
         data = request.get_json()
         if 'conf' not in data:
             return jsonify(message="Missing key 'conf'"), 400
         try:
             content = read_file(CONF_INI)
             conf = settings.set_settings(content,data['conf'][0])
             write_file(CONF_INI,conf)
             new_conf = settings.get_setting(CONF_INI)
             return jsonify(conf=new_conf), 200
         except IOError as e:
             return jsonify(message=str(e)), 500
