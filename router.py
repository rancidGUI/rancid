from flask import jsonify, request, abort
from flask.views import MethodView
from reader_writer.reader import read_csv_file
from reader_writer.writer import write_file
from reader_writer.reader import rewrite_out
from router_db import router_db
from router_db.router_db import get_machine_index
from utils import check_file_access, check_json_key
from rancid_conf.rancid_conf import get_value
from rancid_conf.rancid_conf import check_value
from reader_writer.reader import read_file
from router_db.router_db import get_machine_index
ROUTER_FILE_PREFIX = get_value(read_file("./conf.ini"),"ROUTER_DB_DIR")


class Router(MethodView):

    def get(self, param):

        path = ROUTER_FILE_PREFIX + param + '/router.db'
        b, msg = check_file_access(path)
        if not b:
            return jsonify(message=msg), 400

        try:
            machines = read_csv_file(path)
            machine_ro = rewrite_out(machines)
            return jsonify(machines=machine_ro), 200
        except IOError as e:
            return jsonify(message=str(e)), 500

    def post(self):
        data = request.get_json()
        if check_value(data['ip']) == 1:
            return jsonify(message="BAD FORMAT IP"), 400
        b, msg = check_json_key(data, 'group_name', 'ip', 'type', 'status')
        if not b:
            return jsonify(message='Missing key \'%s\'' % msg), 400
        path = ROUTER_FILE_PREFIX + data["group_name"] + '/router.db'
        b, msg = check_file_access(path)
        if not b:
            return jsonify(message=msg), 400
        try:
            machines = read_csv_file(path)
            idx = get_machine_index(machines, data['ip'])
            if idx is not -1:
                return jsonify(message='Device \'%s\' Already exists' % data['ip']), 400

            router_db.add_machine(path, data['ip'], data['type'], data['status'])
            return jsonify(machine=data), 200
        except IOError as e:
            return jsonify(message=str(e)), 500

    def delete(self):
        data = request.get_json()
        b, msg = check_json_key(data, 'group_name', 'ip')
        if not b:
            return jsonify(message='Missing key \'%s\'' % msg), 400

        path = ROUTER_FILE_PREFIX + data["group_name"] + '/router.db'
        b, msg = check_file_access(path)
        if not b:
            return jsonify(message=msg), 400

        try:
            machines = read_csv_file(path)

            idx = get_machine_index(machines, data['ip'])
            if idx is -1:
                return jsonify(message='Device \'%s\' does not exists' % data['ip']), 400

            machines = router_db.remove_machine(machines, idx)

            for index in range(len(machines)):
                machines[index] = ';'.join(machines[index])
            with open(path, 'w') as f:
                f.write("\n".join(machines))
                if len(machines) > 0:
                    f.write("\n")

            return jsonify(machine='Device \'%s\' removed' % data['ip']), 200
        except IOError as e:
            return jsonify(message=str(e)), 500

    def put(self, param):
        if param not in ['type', 'status']:
            abort(404)
        data = request.get_json()
        b, msg = check_json_key(data, 'group_name', 'ip', param)
        if not b:
            return jsonify(message='Missing key \'%s\'' % msg), 400

        path = ROUTER_FILE_PREFIX + data["group_name"] + '/router.db'
        b, msg = check_file_access(path)
        if not b:
            return jsonify(message=msg), 400

        try:
            machines = read_csv_file(path)

            idx = get_machine_index(machines, data['ip'])
            if idx is -1:
                return jsonify(message='Machine \'%s\' does not exists' % data['ip']), 400

            b, machines = router_db.update(param, machines, data['ip'], data[param])

            if b is True:
                for index in range(len(machines)):
                    machines[index] = ';'.join(machines[index])
                write_file(path, '\n'.join(machines))
                return jsonify(machines="Device Updated"), 200

        except IOError as e:
            return jsonify(message=str(e)), 500
