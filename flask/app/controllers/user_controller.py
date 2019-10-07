# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_mongoengine import MongoEngine

url_prefix = '/user_mgmt'
app = Blueprint('user', __name__)


@app.route('/')
def data_select():
    return render_template("content/user/index.html")
