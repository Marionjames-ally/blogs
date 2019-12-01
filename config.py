import os

class Config:

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:1234@localhost/'
    QUOTES_API_BASE_URL ='    '
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


Config_options ={
    "development":DevConfig,
    "production":ProdConfig
} 