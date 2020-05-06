from aweblog.extensions import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from flask_login import UserMixin


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10), index=True)
    content = db.Column(db.String(1000), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    catalog = db.Column(db.String(200), index=True)
    comment = db.relationship('Comment')
    comment_count = db.Column(db.Integer, default=0)
    love_count = db.Column(db.Integer, default=0)
    read_count = db.Column(db.Integer, default=0)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(10))
    content = db.Column(db.String(200), default='写得太完美了')
    email = db.Column(db.String(100))
    site = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean)
    qualified = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    reply_count = db.Column(db.Integer, default=0)
    love_count = db.Column(db.Integer, default=0)
    # post一对多
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    # reply一对一
    reply = db.relationship('Reply', uselist=False)


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    Comment = db.relationship('Comment')


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


@event.listens_for(Comment, 'after_insert')
@event.listens_for(Comment, 'after_delete')
def update_comment_cn(*args, **kwargs):
    db.session.execute(
        'update Post  set comment_count=(select count(1) from Comment   where Post.id = Comment.post_id)')


@event.listens_for(Comment, 'after_insert')
@event.listens_for(Comment, 'after_delete')
def update_reply_cn(*args, **kwargs):
    db.session.execute(
        'update Comment  set reply_count=(select count(1) from Reply   where Comment.id = Reply.comment_id)')
