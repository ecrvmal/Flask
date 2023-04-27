from datetime import datetime
from flask import Flask


from blog import commands
from blog.extensions import db, login_manager
from blog.models import User, Article

# from blog.user.views import user
# from blog.article.views import article
# from blog.auth.views import auth



def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('blog.config')
    # all these below moved to blog/config.py
    # app.config['SECRET_KEY'] = 'z#if^%-_2j9o9*tjxn(^c3k(#q_gonx^nyf6m7_=$x@y&kqw2r'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    register_extensions(app)
    register_blueprint(app)
    register_commands(app)
    return app

def register_extensions(app):
    db.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprint(app: Flask):

    from blog.auth.views import auth
    from blog.user.views import user
    from blog.article.views import article

    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(auth)

def register_commands(app: Flask):
    app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.create_users)
    app.cli.add_command(commands.create_articles)




