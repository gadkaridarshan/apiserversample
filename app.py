# -*- coding: utf-8 -*-
# ===================================
# main app.py for running Flask
# Author        : Darshan Gadkari
# Created       : Jun 2019
# ===================================
from flask import Flask
from blueprints.Blueprint import blueprint
from dotenv import load_dotenv
import os


# load env variables
load_dotenv('settings/.env')

app = Flask(__name__)

# register blueprint
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(host=os.getenv('HOST_IP'))
