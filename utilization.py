from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy


def initializeAppAndDb(__name__):
    # App Initialization
    app = Flask(__name__)

    app.config.from_pyfile('./config/appconfig.cfg')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{app.config['PG_USER']}:{app.config['PG_PASSWORD']}@{app.config['PG_HOST']}:{app.config['PG_PORT']}/{app.config ['PG_DATABASE']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'secret'
    db = SQLAlchemy(app)

    return app,db


def make_response(rv):
    resp = Response(rv)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp
