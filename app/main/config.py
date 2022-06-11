import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir: str = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG: bool = False
    # Swagger
    RESTX_MASK_SWAGGER: bool = False



class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class TestingConfig(Config):
    DEBUG: bool = True
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class ProductionConfig(Config):
    DEBUG: bool = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key: str = Config.SECRET_KEY
