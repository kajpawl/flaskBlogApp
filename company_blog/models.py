from werkzeug.routing import ValidationError

from company_blog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self, user_id=None):
        json_user = {
            'url': url_for('users_api.get_user', username=self.username),
            'username': self.username,
            'posts_url': url_for('users_api.get_user_posts', username=self.username),
            'posts_count': len(self.posts)
        }
        if user_id is not None and user_id == self.id:
            json_user['email'] = self.email
        return json_user

    def __repr__(self):
        return f"Username {self.username}"


class BlogPost(db.Model):
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def to_json(self):
        json_post = {
            'url': url_for('blog_posts_api.get_post', post_id=self.id),
            'date': self.date,
            'title': self.title,
            'text': self.text,
            'author': self.author.username,
            'author_url': url_for('users_api.get_user', username=self.author.username)
        }
        return json_post

    @staticmethod
    def from_json(json_post, user_id):
        title = json_post.get('title')
        text = json_post.get('text')

        if title is None or title == '':
            raise ValidationError('Post has no title.')
        if text is None or text == '':
            raise ValidationError('Post has no text.')

        return BlogPost(title=title,
                        text=text,
                        user_id=user_id)

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- {self.title}"
