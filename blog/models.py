from datetime import datetime

from sqlalchemy import Table, ForeignKey

from sqlalchemy.orm import relationship
from blog.app import db
from flask_login import UserMixin


article_tag_associations_table = Table('article-tag-associations',
                                       db.metadata,
                                       db.Column('article_id', db.Integer, ForeignKey('articles.id'), nullable=False),
                                       db.Column('tag_id', db.Integer, ForeignKey('tags.id'), nullable=False),
                                       )


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # optional
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    is_staff = db.Column(db.Boolean, default=False)
    author = relationship("Author", uselist=False, back_populates='user')     # 1:1

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"


class Article(db.Model):
    __tablename__ = 'articles'  # optional
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow )
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)     # 1:n relation
    author = db.relationship('Author', back_populates="articles")           # creates list article.user
    tags = db.relationship('Tag', secondary=article_tag_associations_table, back_populates='articles')



class Author(db.Model):
    __tablename__ = 'authors'  # optional
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))       # 1:1 relatiom
    user = relationship('User', back_populates='author')             # 1:1 relation
    articles = db.relationship("Article",back_populates="author")    # 1:n relation


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    articles = db.relationship('Article', secondary=article_tag_associations_table, back_populates='tags')


