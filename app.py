from flask import Flask, Response
from models import db

# App Initialization
app = Flask(__name__)
app.config.from_pyfile('./config/appconfig.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{app.config['PG_USER']}:{app.config['PG_PASSWORD']}@{app.config['PG_HOST']}:{app.config['PG_PORT']}/{app.config ['PG_DATABASE']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
app.app_context().push()
db.init_app(app)
db.create_all()


#Catch undefined paths
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return make_response("Server is up! path: {}".format(path))

# Prepare response format
def make_response(rv):
    resp = Response(rv)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp