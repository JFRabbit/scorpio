from test_dependency.project_demo.db import *

"""
    define Database CRUD 
"""


def create(manager: MySQLManager):
    sql = ""
    return manager.execute(sql)


def update(manager: MySQLManager):
    sql = ""
    return manager.execute(sql)


def retrieve(manager: MySQLManager):
    sql = ""
    return manager.find(sql)


def delete(manager: MySQLManager):
    sql = ""
    return manager.execute(sql)
