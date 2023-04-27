from werkzeug.security import generate_password_hash
from blog.extensions import db
import click


# the there is migrations, the init-db don't need

@click.command('init-db')
def init_db():
    from wsgi import app

    # import models for creating tables
    from blog.models import User

    db.create_all(app=app)


@click.command('create-users')
def create_users():
    from blog.models import User
    from wsgi import app

    with app.app_context():
        db.session.add(
            User(username='user1', email='user1@mail.ru', password=generate_password_hash('123'))
        )
        db.session.add(
            User(username='user2', email='user2@mail.ru', password=generate_password_hash('123'))
        )
        db.session.add(
            User(username='user3', email='user3@mail.ru', password=generate_password_hash('123'))
        )
        db.session.add(
            User( username='user4', email='user4@mail.ru', password=generate_password_hash('123'))
        )
        db.session.add(
            User(username='user5', email='user5@mail.ru', password=generate_password_hash('123'))
        )
        db.session.commit()



@click.command('create-articles')
def create_articles():
    from blog.models import Article
    from wsgi import app

    with app.app_context():
        db.session.add(
            Article(title='Ecology in Country',
                    text='Ecology is the biggest problem in Africa countries', author_id=5 )
        )
        db.session.add(
            Article(title='Alcoholism in Europe',
                    text='British Scientists decided that the more we drink, the less remains',
                    author_id=2, )
        )
        db.session.add(
            Article(title='Weather on SouthPole',
                    text='There is a stable weather on the South Pole. Average temperature is about - 60 degrees of '
                         'Celsius', author_id=3, )
        )
        db.session.add(
            Article(title='About the dangers of learning',
                    text='England scientists discovered that that more people study mathematics the less they sleep',
                    author_id=1, )
        )
        db.session.add(
            Article(title='About Cats',
                    text='People thinks that cats are the most beauty animals in the world',
                    author_id=4, )
        )

        db.session.commit()


@click.command('create-init-tags')
def create_init_tags():
    from blog.models import Tag
    from wsgi import app

    with app.app_context():
        tags = ('flask','django','python', 'gb', 'sqlite' )
        for item in tags:
            db.session.add(Tag(name=item))
        db.session.commit()
    click.echo(f'Created tags : {", ".join(tags)}')






