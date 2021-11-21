
from datetime import datetime
import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

# Model Class for Postgres integration
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), unique=True, nullable=False)
    last_name = db.Column(db.String(40), unique=True, nullable=False)
    blog_amount = db.Column(db.Integer, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.blog_amount = 0
        self.date_joined = datetime.now()

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=True, nullable=False)
    content = db.Column(db.String(200), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String(40), nullable=False)
    tags = db.Column(db.String(200), nullable=False)
    category = db.Column(db.Integer, nullable=False)
    author = db.Column(db.Integer, nullable=False)

    def __init__(self, title, content, image, tags, category, author):
        self.title = title
        self.content = content
        self.date_created = datetime.now()
        self.image = image
        self.tags = tags
        self.category = category
        self.author = author
