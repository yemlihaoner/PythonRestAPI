import os
from flask import request, jsonify
import sqlalchemy
from models import Blogs, Category, Author
from app import make_response, db, app
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

ALLOWED_EXTENSIONS = set(['png', 'jpg'])

#loads .env variables
load_dotenv()

#checks if file format is allowed for upload opertaions
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#save the recieved image and return url
def save_image(files):
    file = files['image']
    if file and file.filename != '' and allowed_file(file.filename):
        #set cloud related information from .env
        cloudinary.config(cloud_name = os.getenv("CLOUD_NAME"), api_key=os.getenv("API_KEY"), 
            api_secret=os.getenv("API_SECRET"))
        
        upload_result = cloudinary.uploader.upload(file)
        app.logger.info(upload_result)
        return upload_result["secure_url"]
    return "no-image"

#Get all the blogs
@app.route('/blog', methods=['GET'])
def get_blogs():
    blogs = []
    for blog in db.session.query(Blogs).all():
        del blog.__dict__['_sa_instance_state']
        blogs.append(blog.__dict__)
    return jsonify(blogs)

#Get the spesific blog
@app.route('/blog/<id>', methods=['GET'])
def get_blog(id):
    try:
        blog = Blogs.query.get(id)
        if(type(blog) is Blogs):
            del blog.__dict__['_sa_instance_state']
            return jsonify(blog.__dict__)
        return make_response("The blog is not found")
    
    except sqlalchemy.exc.DataError as e:
        return make_response("Please control your inputs. id, category and author variables have to be numbers. \nMessage: {}".format(e))


#Create a new blog 
@app.route('/blog', methods=['POST'])
def create_blog():
    try:
        body = request.form
        image_path = save_image(request.files)
        blog = Blogs(body['title'], body['content'], image_path, body['tags'], body['category'],body['author'])
        
        category = Category.query.get(blog.category)
        author = Author.query.get(blog.author)

        #Check if referenced category and author exists 
        if(type(category) is Category and type(author) is Author):
            db.session.query(Author).filter_by(id=blog.author).update({Author.blog_amount:author.blog_amount + 1})
            db.session.add(blog)
            db.session.commit()
            return make_response("The blog is created")
        return make_response("The category or author does not exist related to given ids")
    
    except sqlalchemy.exc.DataError as e:
        return make_response("Please control your inputs. Category and author variables have to be numbers. \nMessage: {}".format(e))
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        return make_response("Please control your inputs. Title and Content variables have to be unique values. \nMessage: {}".format(e))
    except KeyError as e:
        return make_response("Please control your input names. \nMessage: {}".format(e))


#Update the blog with the given id
@app.route('/blog/<id>', methods=['PUT'])
def update_blog(id):
    try:
        body = request.form
        image_path = save_image(request.files)
        blog = Blogs.query.get(id)
        if image_path == "no-image":
            image_path = blog.image
        
        updated_blog = Blogs(body['title'], body['content'], image_path, body['tags'], body['category'],body['author'])
        category = Category.query.get(updated_blog.category)
        author = Author.query.get(blog.author)
        updated_author = Author.query.get(updated_blog.author)

        #Check if referenced category and author exists 
        if(type(updated_blog) is Blogs and type(category) is Category and type(author) is Author):
            if(blog.author is not updated_blog.author):
                db.session.query(Author).filter_by(id=blog.author).update({Author.blog_amount:author.blog_amount - 1})
                db.session.query(Author).filter_by(id=updated_blog.author).update({Author.blog_amount:updated_author.blog_amount + 1})
            
            db.session.query(Blogs).filter_by(id=id).update(
                {Blogs.title: updated_blog.title, Blogs.content: updated_blog.content, Blogs.image: updated_blog.image,
                Blogs.tags: updated_blog.tags, Blogs.category: updated_blog.category, Blogs.author: updated_blog.author})
            db.session.commit()
            return make_response("The blog is updated")
        return make_response("The category or author does not exist related to given ids. ")
    
    except sqlalchemy.exc.DataError as e:
        return make_response("Please control your inputs. id, category and author variables have to be numbers. \nMessage: {}".format(e))
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        return make_response("Please control your inputs. Title and Content variables have to be unique values. \nMessage: {}".format(e))
    except KeyError as e:
        return make_response("Please control your input names. \nMessage: {}".format(e))

#Delete the blog with the given id
@app.route('/blog/<id>', methods=['DELETE'])
def delete_blog(id):
    try:
        blog = Blogs.query.get(id)
        author = Author.query.get(blog.author)
        if(type(blog) is Blogs):
            db.session.query(Author).filter_by(id=blog.author).update({Author.blog_amount:author.blog_amount - 1})
            db.session.query(Blogs).filter_by(id=id).delete()
            db.session.commit()
            return make_response("The blog is deleted")
        return make_response("The blog is not found")
    
    except sqlalchemy.exc.DataError as e:
        return make_response("The id is in invalid form. Please only use numbers. \nMessage: {}".format(e))
