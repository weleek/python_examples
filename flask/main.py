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

import os, sys, docopt
from flask import Flask, Blueprint, request, jsonify, render_template, Response

MAIN_DIR = '/'.join(__file__.split('/')[:-1])
app = Flask(__name__, template_folder=f'{MAIN_DIR}/app1/templates', static_folder=f'{MAIN_DIR}/app1/static')

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
    print('TEST')
    return render_template("base.html")

@app.route('/content')
def content():
    return render_template("content/content.html", message="테스트 메세지", contacts=["q", "w", "e", "r"])


if __name__ == '__main__':
    try:
        args = argv_init(sys.argv[1:])

        if args['run']:
            init(args)
            app.run()

    except KeyboardInterrupt:
        print('Program Exit...')
        sys.exit(0)
    except Exception as err:
        print(f'EXCEPTION : {err}')

