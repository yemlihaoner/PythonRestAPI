from flask import request, jsonify
from app import make_response, db, app
from models import Author
import sqlalchemy

#Get all the authors
@app.route('/author', methods=['GET'])
def get_authors():
    authors = []
    for author in db.session.query(Author).all():
        del author.__dict__['_sa_instance_state']
        authors.append(author.__dict__)
    return jsonify(authors)


#Get the spesific author
@app.route('/author/<id>', methods=['GET'])
def get_author(id):
    try:
        author = Author.query.get(id)
        if(type(author) is Author):
            del author.__dict__['_sa_instance_state']
            return jsonify(author.__dict__)
        return make_response("The author is not found")
    except sqlalchemy.exc.DataError as e: 
        return make_response("The id is in invalid form. Please only use numbers. \nMessage: {}".format(e))



#Create a new author 
@app.route('/author', methods=['POST'])
def create_author():
    try:
        body = request.get_json()
        db.session.add(Author(body['first_name'], body['last_name']))
        db.session.commit()
        return make_response("The author is created")
    except KeyError as e:
        return make_response("Please control your input names. \nMessage: {}".format(e))


#Update the author with the given id
@app.route('/author/<id>', methods=['PUT'])
def update_author(id):
    try:
        body = request.get_json()
        db.session.query(Author).filter_by(id=id).update(
            dict(name=body['first_name'], description=body['last_name']))
        db.session.commit()
        return make_response("The author is updated")
    except sqlalchemy.exc.DataError as e:
        return make_response("The id is in invalid form. Please only use numbers. \nMessage: {}".format(e))
    except KeyError as e:
        return make_response("Please control your input names. \nMessage: {}".format(e))



#Delete the author with the given id
@app.route('/author/<id>', methods=['DELETE'])
def delete_author(id):
    try:
        author = Author.query.get(id)
        if(type(author) is Author):
            if(author.blog_amount is not 0):
                return make_response("The author is not deleted. There are blogs recorded under this category.")

            db.session.query(Author).filter_by(id=id).delete()
            db.session.commit()
            return make_response("The author is deleted")
        return make_response("The author is not found")
    except sqlalchemy.exc.DataError as e:
        return make_response("The id is in invalid form. Please only use numbers. \nMessage: {}".format(e))
