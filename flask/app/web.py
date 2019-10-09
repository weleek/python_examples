# -*- coding: utf-8 -*-
import os
import sys
import datetime
import importlib
import signal

import psutil
from flask import Flask

MAIN_DIR = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/'))
PARENT_DIR = '/'.join(MAIN_DIR.split('/')[:-1])
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from app.exceptions.exceptions import ProcessException


def web_init(app, argv):
    if argv['--debug']:
        app.jinja_env.auto_reload = argv['--debug']
        app.debug = argv['--debug']
        app.env = 'development'
    blueprint_init(app)


def blueprint_init(app):
    for controller in os.listdir(f'{MAIN_DIR}/controllers'):
        if controller.find('__') != -1:
            continue

        controller = importlib.import_module(f"app.controllers.{controller.replace('.py', '')}")
        app.register_blueprint(controller.app, url_prefix=controller.url_prefix)


def create_app(argv):
    app = Flask(__name__, template_folder=f'{MAIN_DIR}/frontend/templates',
    static_folder=f'{MAIN_DIR}/frontend/static', static_url_path='/static')
    web_init(app, argv)
    return app


def check_web():
    for p in psutil.process_iter():
        if p.name() == 'gunicorn' and ''.join(p.cmdline()).find('flask_app') != -1:
            return True
    return False


def web_start(argv):
    print("Web service start...")
    if check_web():
        raise ProcessException('Web service is already running...')

    cmds = []
    cmds.append('gunicorn')
    cmds.append('--name=flask_app')
    cmds.append(f'--chdir={PARENT_DIR}')
    cmds.append(f'\'app.web:create_app({{"--debug": {argv["--debug"]} }})\'')
    cmds.append(f'--bind=0.0.0.0:{argv["server"]["port"]}')
    cmds.append('--daemon')
    cmds.append('--workers=2')
    cmds.append(f'--log-level={argv["logging"]["level"]}')
    cmds.append(f'--access-logfile="{PARENT_DIR}/logs/web_access.log"')
    cmds.append(f'--error-logfile="{PARENT_DIR}/logs/web_error.log"')
    cmds.append('--reload' if argv["--debug"] else '')
    cmd = ' '.join(cmds)
    os.system(cmd)

def web_shutdown(argv):
    print("Web service shutdown...")
    if not check_web():
        raise ProcessException('Web service is not running...')

    for p in psutil.process_iter():
        if p.name() == 'gunicorn' and ''.join(p.cmdline()).find('flask_app') != -1:
            os.kill(p.pid, signal.SIGTERM)


def web_status(argv):
    print("Web service status...")
    if not check_web():
        raise ProcessException('Web service is not running...')

    for p in psutil.process_iter():
        if p.name() == 'gunicorn' and ''.join(p.cmdline()).find('flask_app') != -1:
            print(f"{p.name()} {p.username()} {p.pid} {p.ppid()}", end=" ")
            print(f"{datetime.datetime.fromtimestamp(p.create_time()).strftime('%Y-%m-%d %H:%M:%S')}", end=" ")
            print(f"{' '.join(p.cmdline())}")


def main(argv):
    try:
        if argv['--status']:

            web_status(argv)

        elif argv['--start']:

            web_start(argv)

        elif argv['--stop']:

            web_shutdown(argv)

        else:
            raise ProcessException("Check the options...")

    except Exception as err:
        raise err
