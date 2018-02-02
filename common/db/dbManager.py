# coding: utf-8

import MySQLdb
import psycopg2

from common.log.baseLog import BaseLog
from config.env_db import *


class DBManager(object):
    def __init__(self, connection_name: str, func):
        self.log = BaseLog(DBManager.__name__).log
        """初始化：
                1 加载配置文件
                2 连接数据库
                3 设置光标
        """

        try:
            self.__connect = func(connection_name)
        except Exception as e:
            self.__isClose = True
            self.log.error(e)
            raise e

        self.__cursor = self.__connect.cursor()
        self.__isClose = False
        self.log.info("Connected")

    def __del__(self):
        self.close()

    def close(self):
        """关闭数据库连接"""
        if self.__isClose is False:
            self.log.info("Close connection...")
            self.__connect.close()
            self.__isClose = True
            self.log.info("Closed")

    def find(self, sql, find_size=0, find_all=True):
        """查询：
            如果all = True 返回所有数据
            否则只返回第一条数据
        """
        self.log.info("Execute query sql: %s" % sql)
        self.__cursor.execute(sql)

        if find_size > 0:
            return self.__cursor.fetchmany(find_size)

        if find_all:
            return self.__cursor.fetchall()

        return self.__cursor.fetchone()

    def execute(self, sql):
        """更改：
            可适用于增、删、改
        """
        try:
            self.log.info("Execute change: %s" % sql)
            num = self.__cursor.execute(sql)
            self.__connect.commit()
            return num
        except Exception as e:
            self.log.warning("Modify Database Failed: %s" % e)
            self.__connect.rollback()
            return None

    @staticmethod
    def sql_result_2_dict(select_items: tuple, result_items: tuple):
        """将查询结果匹配查询的key"""
        if len(select_items) is 0 or len(result_items) is 0:
            raise Exception("Data length is 0")

        if len(select_items) is not len(result_items[0]):
            raise Exception("Data length different")

        if len(result_items) is 1:
            obj = {}
            for j in select_items:
                obj[j] = result_items[0][select_items.index(j)]

            return obj

        result = []
        for i in result_items:
            obj = {}
            for j in select_items:
                obj[j] = i[select_items.index(j)]

            result.append(obj)

        return result

    @staticmethod
    def dict_2_class(data: dict, target_class: object):
        for k, v in target_class.__dict__.items():  # type: str, object
            try:
                setattr(target_class, k, data[k])
            except KeyError:
                setattr(target_class, k, v)
        return target_class


class MySQLManager(DBManager):
    """ MySQL pip install mysqlclient """

    def __init__(self, connection_name: str):
        super().__init__(connection_name, self.__driver_init)

    def __driver_init(self, connection_name):
        config = MYSQL_CONFIG
        self.log.info("Connect DataBase:[%s]..." % config[connection_name][DB])
        return MySQLdb.connect(
            host=config[connection_name][HOST],
            port=config[connection_name][PORT],
            user=config[connection_name][USER],
            passwd=config[connection_name][PASSWD],
            db=config[connection_name][DB],
            charset=config[connection_name][CHARSET]
        )  # type: MySQLdb.connections.Connection


class PostgreSQLManager(DBManager):
    """ PostgreSQL """

    def __init__(self, connection_name: str):
        super().__init__(connection_name, self.__driver_init)

    def __driver_init(self, connection_name):
        config = POSTGRESQL_CONFIG
        self.log.info("Connect DataBase:[%s]..." % config[connection_name][DB])
        return psycopg2.connect(
            host=config[connection_name][HOST],
            port=config[connection_name][PORT],
            user=config[connection_name][USER],
            password=config[connection_name][PASSWD],
            database=config[connection_name][DB],
        )  # type: psycopg2._ext.connection


if __name__ == '__main__':
    import time

    # mysql
    test_manager = MySQLManager("local")
    time.sleep(1)

    sql_find = 'SELECT * FROM foo'
    print(test_manager.find(sql_find))
    print(test_manager.find(sql_find, False))
    time.sleep(1)

    sql_insert = "INSERT INTO foo(foo_name) VALUE('Tom')"
    print(test_manager.execute(sql_insert))
    print(test_manager.find(sql_find))
    time.sleep(1)

    test_data = test_manager.find(sql_find)  # type: tuple
    effect_num = test_data[-1][0]

    sql_update = "update foo set foo_name = 'Marry' where foo_id = '%d'" % effect_num
    print(test_manager.execute(sql_update))
    print(test_manager.find(sql_find))
    time.sleep(1)

    sql_delete = "delete from foo where foo_id='%d'" % effect_num
    print(test_manager.execute(sql_delete))
    print(test_manager.find(sql_find))
    time.sleep(1)

    test_manager.close()

    # postgresql
    test_ps = PostgreSQLManager(LOCAL)

    test_data = test_ps.find("SELECT * FROM foo")
    print(test_data)
    test_ps.close()
