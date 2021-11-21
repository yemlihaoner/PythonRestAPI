from flask import request, jsonify
from models import Blogs, Category, Author
from app import make_response, db, app

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
    blog = Blogs.query.get(id)
    if(type(blog) is Blogs):
        del blog.__dict__['_sa_instance_state']
        return jsonify(blog.__dict__)
    return make_response("The blog is not found")

#Add a new category 
@app.route('/blog', methods=['POST'])
def create_blog():
    body = request.get_json()
    blog = Blogs(body['title'], body['content'], "temp-image", body['tags'], body['category'],body['author'])
    category = Category.query.get(blog.category)
    author = Author.query.get(blog.author)

    #Check if referenced category and author exists 
    if(type(category) is Category and type(author) is Author):
        db.session.query(Author).filter_by(id=blog.author).update({Author.blog_amount:author.blog_amount + 1})
        db.session.add(blog)
        db.session.commit()
        return make_response("The blog is created")
    return make_response("The category or author is not exist related to given ids")

#Update the blog with the given id
@app.route('/blog/<id>', methods=['PUT'])
def update_blog(id):
    body = request.get_json()
    updated_blog = Blogs(body['title'], body['content'], "temp-image", body['tags'], body['category'],body['author'])
    blog = Blogs.query.get(id)
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
    return make_response("The category or author is not exist related to given ids")

#Delete the blog with the given id
@app.route('/blog/<id>', methods=['DELETE'])
def delete_blog(id):
    blog = Blogs.query.get(id)
    author = Author.query.get(blog.author)
    if(type(blog) is Blogs):
        db.session.query(Author).filter_by(id=blog.author).update({Author.blog_amount:author.blog_amount - 1})
        db.session.query(Blogs).filter_by(id=id).delete()
        db.session.commit()
        return make_response("The blog is deleted")
    return make_response("The blog is not found")
