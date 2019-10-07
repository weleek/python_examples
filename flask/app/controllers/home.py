# -*- coding: utf-8 -*-
import os
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_mongoengine import MongoEngine

MODULE_HOME = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/'))
url_prefix = '/'
app = Blueprint('home', __name__)

@app.route('/')
def home():
    return render_template("base.html")
