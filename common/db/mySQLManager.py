# coding: utf-8

import MySQLdb

from common.log.baseLog import BaseLog
from common.db.dbConstants import *
from config.env_db import MYSQL_CONFIG
from common.util.jsonFormat import *


class MySQLManager(object):
    """数据库操作类 pip install mysqlclient """

    def __init__(self, connection_name: str):
        self.log = BaseLog(MySQLManager.__name__).log
        """初始化：
                1 加载配置文件
                2 连接数据库
                3 设置光标
        """

        try:
            config = MYSQL_CONFIG
            self.log.info("Connect DataBase:[%s]..." % config[connection_name][DB])
            self.__connect = MySQLdb.connect(
                host=config[connection_name][HOST],
                port=config[connection_name][PORT],
                user=config[connection_name][USER],
                passwd=config[connection_name][PASSWD],
                db=config[connection_name][DB],
                charset=config[connection_name][CHARSET]
            )
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

    def execute(self, sql):
        """执行SQL"""
        self.log.info("Execute sql: %s" % sql)
        self.__cursor.execute(sql)

    def find(self, sql, find_all=True):
        """查询：
            如果all = True 返回所有数据
            否则只返回第一条数据
        """
        self.log.info("Execute query sql: %s" % sql)
        self.execute(sql)
        if find_all:
            return self.__cursor.fetchall()
        return self.__cursor.fetchone()

    def change(self, sql):
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
            return 0


def sql_result_2_dict(select_items: tuple, result_items: tuple):
    if len(select_items) is 0 or len(result_items) is 0:
        raise Exception("Data length is 0")

    if len(select_items) is not len(result_items[0]):
        raise Exception("Data length different")

    if len(result_items) is 1:
        obj = {}
        for j in select_items:
            obj[j] = result_items[0][select_items.index(j)]

        test_manager.log.info(json_format(obj))
        return obj

    result = []
    for i in result_items:
        obj = {}
        for j in select_items:
            obj[j] = i[select_items.index(j)]

        result.append(obj)

    test_manager.log.info(json_format(result))
    return result


def dict_2_class(data: dict, target_class: object):
    for k, v in target_class.__dict__.items():  # type: str, object
        try:
            setattr(target_class, k, data[k])
        except KeyError:
            setattr(target_class, k, v)
    return target_class


if __name__ == '__main__':
    import time

    test_manager = MySQLManager("local")
    time.sleep(1)

    sql_find = 'SELECT * FROM foo'
    test_manager.log.info(test_manager.find(sql_find))
    test_manager.log.info(test_manager.find(sql_find, False))
    time.sleep(1)

    sql_insert = "INSERT INTO foo(foo_name) VALUE('Tom')"
    test_manager.log.info(test_manager.change(sql_insert))
    test_manager.log.info(test_manager.find(sql_find))
    time.sleep(1)

    test_data = test_manager.find(sql_find)  # type: tuple
    effect_num = test_data[-1][0]

    sql_update = "update foo set foo_name = 'Marry' where foo_id = '%d'" % effect_num
    test_manager.log.info(test_manager.change(sql_update))
    test_manager.log.info(test_manager.find(sql_find))
    time.sleep(1)

    sql_delete = "delete from foo where foo_id='%d'" % effect_num
    test_manager.log.info(test_manager.change(sql_delete))
    test_manager.log.info(test_manager.find(sql_find))
    time.sleep(1)

    test_manager.close()
