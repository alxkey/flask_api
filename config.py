import os
from environs import Env
from urllib.parse import urlparse

if os.environ.get("ENV") == "production":
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_URL = os.environ.get("DATABASE_URL")
else:
    env = Env()
    env.read_env()
    SECRET_KEY = env("key")
    DATABASE_URL = env("database_url")

connect = urlparse(DATABASE_URL)

USER = connect.username
PASSWORD = connect.password
DB_NAME = connect.path[1:]
HOST = connect.hostname
PORT = connect.port

