# -*- coding: utf-8 -*-
"""Flask and mongodb sample web project.

    Usage:
        main.py -h | --help | --version
        main.py run [--debug]

    Commands:
        run         running app1.

    Options:
        -h --help   help document.
        --version   verbose mode
        --debug     development(templates auto reload) mode.
"""

import docopt
import sys
import mongoengine as me
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_mongoengine import MongoEngine

MAIN_DIR = '/'.join(__file__.split('/')[:-1])
app = Flask(__name__, template_folder=f'{MAIN_DIR}/app1/templates', static_folder=f'{MAIN_DIR}/app1/static')
database = None


class User(me.Document):
    userid = me.StringField(required=True)
    username = me.StringField()
    detail = me.StringField()

def argv_init(argv=None):
    return docopt.docopt(__doc__, argv, version='0.0.1')


def init(args):
    web = Blueprint('api', __name__)
    app.register_blueprint(web, url_prefix='/app1')

    if args['--debug']:
        app.jinja_env.auto_reload = args['--debug']
        app.debug = args['--debug']
        app.env = 'development'


@app.route('/')
def home():
    return render_template("base.html")


@app.route('/content')
def content():
    return render_template("content/content.html", message="테스트 메세지", contacts=["q", "w", "e", "r"])


@app.route('/db', methods=['GET'])
def data_select():
    u = User.objects(userid="test")
    return jsonify({"result": u}), 200


@app.route('/db', methods=['POST'])
def data_insert():
    data = request.get_json()
    userid = data['userid']
    username = data['name']
    detail = data['detail']

    u = User(userid=userid, username=username, detail=detail)
    u.save()
    return jsonify({"result": "OK"}), 200


def database_init():
    app.config['MONGODB_SETTINGS'] = {
        'db': 'admin',
        'host': 'localhost',
        'port': 27017,
        'username': 'admin',
        'password': 'admin'
    }
    database = MongoEngine()
    database.init_app(app)


if __name__ == '__main__':
    try:
        args = argv_init(sys.argv[1:])

        if args['run']:
            init(args)
            database_init()
            app.run()

    except KeyboardInterrupt:
        print('Program Exit...')
        sys.exit(0)
    except Exception as err:
        print(f'EXCEPTION : {err}')
