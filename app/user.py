from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


class Quote:
    '''
    Quote class to define quote Objects
    '''

    def __init__(self, id, author, quote, permalink):
        self.id = id
        self.author = author
        self.quote = quote
        self.permalink = permalink



class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    bio = db.Column(db.String(255))
    password = db.Column(db.String(70), nullable=False)
    blogs = db.relationship('Blog', backref='author', lazy="dynamic")
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)


def __repr__(self):
    return f'User {self.username}', '{self.image}'


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(110), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.relationship('Comment', backref='pitch', lazy='dynamic')

    @classmethod
    def get_blogs(cls, id):
        blogs = Blog.query.order_by(blog_id=id).desc().all()
        return blogs

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Blog {self.content}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey(
        'blogs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = Blog.query.filter_by(blog_id=id).all()
        return comments

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()