from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy

from utilization import initializeAppAndDb, make_response

# App Initialization
app,db = initializeAppAndDb(__name__)

# Model Class for Postgres integration
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

#Creates defined tables above
db.create_all()

#Catch undefined paths
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return make_response("Server is up! path: {}".format(path))

#Get all the items
@app.route('/items', methods=['GET'])
def get_items():
    items = []
    for item in db.session.query(Item).all():
        del item.__dict__['_sa_instance_state']
        items.append(item.__dict__)
    return jsonify(items)

#Get the spesific item
@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    item = Item.query.get(id)
    if(type(item) is Item):
        del item.__dict__['_sa_instance_state']
        return jsonify(item.__dict__)
    return make_response("item is not found")

#Add a new item 
@app.route('/items', methods=['POST'])
def create_item():
    body = request.get_json()
    db.session.add(Item(body['title'], body['content']))
    db.session.commit()
    return make_response("item created")

#Update the item with the given id
@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    body = request.get_json()
    db.session.query(Item).filter_by(id=id).update(
        dict(title=body['title'], content=body['content']))
    db.session.commit()
    return make_response("item updated")

#Delete the item with the given id
@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    if(type(item) is Item):
        db.session.query(Item).filter_by(id=id).delete()
        db.session.commit()
        return make_response("item deleted")
    return make_response("item is not found")