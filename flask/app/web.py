# -*- coding: utf-8 -*-
import os
from flask import Flask
import importlib

MAIN_DIR = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/'))
app = Flask(__name__, template_folder=f'{MAIN_DIR}/app1/frontend/templates',
            static_folder=f'{MAIN_DIR}/app1/frontend/static')
database = None


def blueprint_init():
    for controller in os.listdir(f'{MAIN_DIR}/app1/controller'):
        if controller.find('__') != -1:
            continue

        controller = importlib.import_module(f"app1.controller.{controller.replace('.py', '')}")
        app.register_blueprint(controller.app, url_prefix=controller.url_prefix)


def init(args):
    if args['--debug']:
        app.jinja_env.auto_reload = args['--debug']
        app.debug = args['--debug']
        app.env = 'development'
    blueprint_init()


def main(args):
    try:
        init(args)
        app.run()
    except Exception as err:
        raise err
