from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager

class Quote:
    '''
    quote class to define quote Objects
    '''

    def __init__(self,id,author,quote,permalink):
        self.id =id
        self.author = author
        self.quote = quote
        self.permalink = permalink
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(70), nullable=False)
    blogs = db.relationship('Blog', backref='author', lazy="dynamic")
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    pass_secure = db.Column(db.String(255))
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
		
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