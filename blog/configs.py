import os
from dotenv import load_dotenv
from sqlalchemy.dialects import postgresql

from blog.enums import EnvType


# load_dotenv()
# ENV = os.getenv('FLASK_ENV', default=EnvType.production)


class BaseConfig(object):
    DEBUG = False
    # DEBUG = ENV == EnvType.development
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = "sqlite:///memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'z#if^%-_2j9o9*tjxn(^c3k(#q_gonx^nyf6m7_=$x@y&kqw2r'


class DevConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@database:5432/blog"

class TestConfig(BaseConfig):
    TESTING = True





SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False