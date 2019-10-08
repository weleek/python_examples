# -*- coding: utf-8 -*-
import os
import psutil
import datetime
from pathlib import Path
from flask_mongoengine import MongoEngine
from app.exceptions.exceptions import ProcessException

MAIN_DIR = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/'))
DATABASE_HOME = f'{str(Path.home())}/mongodb/app'


def check_database():
    return ('mongod' in ( p.name() for p in psutil.process_iter()))


def database_init(app):
    app.config['MONGODB_SETTINGS'] = {
        'db': 'admin',
        'host': 'localhost',
        'port': 27017,
        'username': 'admin',
        'password': 'admin'
    }
    database = MongoEngine()
    database.init_app(app)


def database_start():
    print('Database start...')
    if check_database():
        raise ProcessException('Database is already running...')

    if not os.path.exists(f'{DATABASE_HOME}'):
        os.makedirs(f'{DATABASE_HOME}')

    if not os.path.exists(f'{DATABASE_HOME}/logs'):
        os.makedirs(f'{DATABASE_HOME}/logs')

    if not os.access(f'{DATABASE_HOME}/logs', os.W_OK):
        os.chmod(f'{DATABASE_HOME}/logs', 0o777)

    database_cmd = f'mongod --fork --logpath {DATABASE_HOME}/logs/database.log --logappend --dbpath {DATABASE_HOME}'
    os.system(f'{database_cmd}')


def database_shutdown():
    print('Database stop...')
    if not check_database():
        raise ProcessException('Database is not running...')

    os.system(f'mongod --dbpath {DATABASE_HOME} --shutdown')


def database_status():
    print('Database status...')
    if not check_database():
        raise ProcessException('Database is not running...')

    for p in psutil.process_iter():
        if p.name() == 'mongod':
            print(f"{p.name()} {p.username()} {p.pid} {p.ppid()}", end="")
            print(f"{datetime.datetime.fromtimestamp(p.create_time()).strftime('%Y-%m-%d %H:%M:%S')}", end="")
            print(f"{' '.join(p.cmdline())}")


def main(argv=None):
    try:
        if argv['--status']:

            database_status()

        elif argv['--start']:

            database_start()

        elif argv['--stop']:

            database_shutdown()

        else:
            raise ProcessException("Check the options...")

    except Exception as err:
        raise err
