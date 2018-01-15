# coding: utf-8
from common import PROJECT_PATH

DB_CONFIG_PATH = PROJECT_PATH + '/config/db.yaml'

MYSQL = 'mysql'
HOST = 'host'
PORT = 'port'
USER = 'user'
PASSWD = 'passwd'
DB = 'db'
CHARSET = 'charset'

MONGO = 'mongo'

if __name__ == "__main__":
    print(DB_CONFIG_PATH)
