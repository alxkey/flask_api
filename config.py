from environs import Env

env = Env()
env.read_env()

DB_NAME = env.str("database")
USER = env("user")
PASSWORD = env("password")
HOST = env("host")
PORT = env("port")

