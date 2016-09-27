from flask import Flask
from group import Groups
from router import Router
from cloginrc import Cloginrc
from version import Versionning
from saveconf import Rancidrun
from conf import Conf

app = Flask(__name__)


# Enregistrement des routes
app.add_url_rule('/api/groups', view_func=Groups.as_view('groups'), methods=['GET', 'POST', 'DELETE'])

user_view = Router.as_view('router')
rancidrun_view = Rancidrun.as_view('rancidrun')
app.add_url_rule('/api/router/', view_func=user_view, methods=['POST', 'DELETE'])
app.add_url_rule('/api/router/<string:param>', view_func=user_view, methods=['GET', 'PUT'])
app.add_url_rule('/api/cloginrc/<string:param>', view_func=Cloginrc.as_view('cloginrc'), methods=['GET', 'POST', 'DELETE'])
app.add_url_rule('/api/router/<string:param>/<string:param2>/<string:param3>', view_func=Versionning.as_view('version'), methods=['GET'])
app.add_url_rule('/api/save/<string:param>', view_func=rancidrun_view, methods=['GET'])
app.add_url_rule('/api/save/', view_func=rancidrun_view, methods=['POST','DELETE'])
app.add_url_rule('/api/settings/', view_func=Conf.as_view('conf'), methods=['GET','POST','DELETE'])
if __name__ == '__main__':
    app.run(
        # host=app.config.get("HOST", "0.0.0.0"),
        # port=app.config.get("PORT", 6000),
        debug=True
    )
