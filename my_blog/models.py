from flask import current_app
from my_blog import db, login
from datetime import datetime
from flask_login import UserMixin

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model, ):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comment = db.relationship('Comment', backref='commentator', lazy='dynamic')


    def get_reset_token(self, expires_sec=1800):  # IN how many sec, token expires
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('UTF-8')  # creates token, user_id is payload

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return 'User {}'.format(self.username)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text,nullable = False )
    title = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Post {}'.format(self.body)

class Comment(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    c_body = db.Column(db.Text, nullable = False )
    c_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    c_author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return 'Comment{}'.format(self.comment_id)
