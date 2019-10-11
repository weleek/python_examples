# -*- coding: utf-8 -*-
# default libs
import os
import datetime
import importlib
import signal

# 3rd party libs
import psutil
from flask import Flask
from gevent.pywsgi import WSGIServer

# custom develop libs
from exceptions.exceptions import ProcessException

MAIN_DIR = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/'))
PARENT_DIR = '/'.join(MAIN_DIR.split('/')[:-1])


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


def get_pids():
    result = []
    for p in psutil.process_iter():
        try:
            cmdlines = ' '.join(p.cmdline())
            if cmdlines.find('flask_app') != -1 and cmdlines.find('gunicorn') != -1:
                result.append(p.pid)
        except:
            continue
    return result


def check_service():
    return len(get_pids()) > 0


def web_start(argv):
    print("Web service start...")
    if check_service():
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
    if not check_service():
        raise ProcessException('Web service is not running...')

    for pid in get_pids():
        os.kill(pid, signal.SIGTERM)


def web_status(argv):
    print("Web service status...")
    if not check_service():
        raise ProcessException('Web service is not running...')

    for pid in get_pids():
        p = psutil.Process(pid)
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
