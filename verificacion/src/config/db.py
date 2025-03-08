from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()

# Variables de entorno para la conexión a la base de datos
DB_USERNAME = os.getenv('DB_USERNAME', default="user")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="9003")

class DatabaseConfigException(Exception):
    def __init__(self, message='Configuration file is Null or malformed'):
        self.message = message
        super().__init__(self.message)


def database_connection(config, basedir=os.path.abspath(os.path.dirname(__file__))) -> str:
    if not isinstance(config,dict):
        raise DatabaseConfigException
    
    if config.get('TESTING', False) == True:
        return f'sqlite:///{os.path.join(basedir, "database.db")}'
    else:
        return f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/verificacion_db'


def init_db(app: Flask):
    global db 
    db = SQLAlchemy(app)