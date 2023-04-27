from sqlalchemy.orm import relationship
from blog.app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # optional
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    birth_year = db.Column(db.Integer)
    u_articles = db.relationship("Article", back_populates="a_user")          # creates list user.article
    is_staff = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"


class Article(db.Model):
    __tablename__ = 'articles'  # optional
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.String)
    a_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    a_user = db.relationship('User', back_populates="u_articles")           # creates list article.user

