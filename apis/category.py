from flask import request, jsonify
from models import Blogs, Category
from app import make_response, db, app

#Get all the categories
@app.route('/category', methods=['GET'])
def get_categories():
    categories = []
    for category in db.session.query(Category).all():
        del category.__dict__['_sa_instance_state']
        categories.append(category.__dict__)
    return jsonify(categories)

#Get the spesific category
@app.route('/category/<id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if(type(category) is Category):
        del category.__dict__['_sa_instance_state']
        return jsonify(category.__dict__)
    return make_response("The category is not found")

#Add a new category 
@app.route('/category', methods=['POST'])
def create_category():
    body = request.get_json()
    db.session.add(Category(body['name'], body['description']))
    db.session.commit()
    return make_response("The category is created")

#Update the category with the given id
@app.route('/category/<id>', methods=['PUT'])
def update_category(id):
    body = request.get_json()
    db.session.query(Category).filter_by(id=id).update(
        dict(name=body['name'], description=body['description']))
    db.session.commit()
    return make_response("The category is updated")

#Delete the category with the given id
@app.route('/category/<id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    blog = Blogs.query.filter(Blogs.category == id).first()

    if(type(blog) is Blogs):
        return make_response("The category is not deleted. There are blogs recorded under this category.")

    if(type(category) is Category):
        db.session.query(Category).filter_by(id=id).delete()
        db.session.commit()
        return make_response("The category is deleted")
    return make_response("The category is not found")