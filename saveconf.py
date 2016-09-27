from flask import jsonify, request, abort
from flask.views import MethodView
from utils import check_file_access, check_json_key
from rancid_conf.rancid_conf import excecute_cmd
from reader_writer.reader import read_file
from rancid_run import rancid_run

class Rancidrun(MethodView):

    def get(self, param):

        try:
            list_of_cron = rancid_run.get_cronjob(param)
            return jsonify(list_of_cronjob=list_of_cron), 200
        except IOError as e:
            return jsonify(message=str(e)), 500

    def post(self):

        data = request.get_json()
        if 'cron_job' not in data:
            return jsonify(message="Missing key 'cronjob'"), 400
        try:
            status = rancid_run.add_cronjob(data)
            excecute_cmd("rm ./tftp_log.txt")
            return jsonify(message=status), 200
        except IOError as e:
            return jsonify(message=str(e)), 500

    def delete(self):

        data = request.get_json()
        if 'cron_job' not in data:
            return jsonify(message="Missing key 'cronjob'"), 400
        try:
            status = rancid_run.delete_cronjob(data)
            return jsonify(message=status), 200
        except IOError as e:
            return jsonify(message=str(e)), 500
