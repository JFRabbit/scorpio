import re
import datetime

from common.api import *
from common.api.jsonCompare.data import *
from common.api.jsonCompare.compareConstant import *
from common.api.jsonCompare.compareData import *
from common.api.jsonCompare.compareError import *
from common.api.jsonCompare.ruleEnum import *


class Comparator(object):
    def __init__(self):
        self.is_same = True
        self.error_msg = ""
        self.__path = ""
        self.__rule_dict = {}  # type: dict
        self.log = BaseLog(Comparator.__name__).log

    def reset(self):
        self.is_same = True
        self.error_msg = ""
        self.__path = ""
        self.__rule_dict = {}  # type: dict

    def __str__(self):
        if self.is_same:
            return "\nIsSame:\n\t%s" % self.is_same
        return "\nIsSame:\n\t%s\nErrorMsg:%s\n" % (self.is_same, self.error_msg)

    def set_rule(self, key: str, rule: Rule, regex=None):
        """
        Set Compare Rule
        :param key: key of json, default use "root"
        :param rule: Rule Enum
        :param regex: if Rule is MATCH_REGEX
        :return:
        """
        if regex is None:
            self.__rule_dict[key] = rule
        else:
            self.__rule_dict[key] = rule + regex

    def compare(self, expect, actual, is_check_one=False):
        """
        比较字典 expect和actual必须为CompareData或者CompareDataList的实例对象
        :param expect: 预期
        :param actual: 实际
        :param is_check_one: 列表是否仅检查第一项
        :return: True False
        """

        self.__path += PATH_ROOT

        # 判断Response Code

        if expect.code != actual.code:
            self.is_same = False
            self.__set_error(
                CompareError(self.__path, RESPONSE_CODE_DIFF, self.__set_error_msg(expect.code, actual.code)))
            return self
        elif RESPONSE_CODE in self.__rule_dict and self.__rule_dict[RESPONSE_CODE] == Rule.ONLY_CHECK_CODE.value:
            return self

        if isinstance(expect, CompareData):
            self.__compare_json(expect.data, actual.data, is_check_one)

        elif isinstance(expect, CompareDataList):
            self.__compare_list(self.__path, expect.data, actual.data, is_check_one)

        else:
            raise Exception("Only support class compare: CompareData, CompareDataList")

        if len(self.error_msg) != 0:
            self.is_same = False
            pass

        return self

    def __compare_json(self, expect: dict, actual: dict, is_check_one):

        # 对比json object
        self.__compare_obj(PATH_ROOT, expect, actual, is_check_one)

        pass

    def __compare_obj(self, key: str, expect: dict, actual: dict, is_check_one):
        if self.__rule_dict.get(key) == Rule.IGNORE_VALUE.value or self.__rule_dict.get(
                key) == Rule.IS_JSON_OBJECT.value:
            return

        self.__path += PATH_OBJECT + "[%s]" % key

        # 判断Response 的json字段长度
        if self.__rule_dict.get(key) == Rule.IGNORE_OBJECT_KEY_MISS_MATCH.value:
            pass
        else:
            if expect.keys() != actual.keys():
                self.log.info(key)
                self.__set_error(
                    CompareError(self.__path, KEY_NOT_MATCH, self.__set_error_msg(expect.keys(), actual.keys())))
                return

        # 遍历
        index = -1
        current_path = self.__path

        for (k, v) in expect.items():
            index += 1
            self.__path = current_path

            if self.__is_primitive(v):
                if self.__compare_primitive(v, actual.get(k)):
                    pass
                else:
                    self.__path += "[%d][%s]" % (index, k)
                    self.__set_error(CompareError(self.__path, VALUE_DIFF, self.__set_error_msg(v, actual.get(k))))
                continue

            if isinstance(v, dict):
                self.__compare_obj(k, v, actual.get(k), is_check_one)
                continue

            if isinstance(v, list):
                self.__path += PATH_ARRAY + "[%s]" % k
                self.__compare_list(k, v, actual.get(k), is_check_one)
                continue

        pass

    def __compare_list(self, key: str, expect: list, actual: list, is_check_one):
        if self.__rule_dict.get(key) == Rule.IS_JSON_ARRAY.value \
                or expect == Rule.IS_JSON_ARRAY.value \
                or self.__rule_dict.get(key) == Rule.IGNORE_VALUE.value:
            return

        # key += PATH_ROOT

        if is_check_one or self.__rule_dict.get(key) == Rule.IGNORE_ARRAY_SIZE.value:
            if len(expect) == 0 or len(actual) == 0:
                raise Exception("length must > 0 when check one of List")

            self.__path += "[0]"
            i = expect[0]
            if isinstance(i, dict):
                key += SUB_OBJ
                self.__compare_obj(key, i, actual[0], is_check_one)
                return

            if isinstance(i, list):
                self.__path += PATH_ARRAY
                self.__compare_list(key, i, actual[0], is_check_one)
                return

        else:
            if len(expect) != len(actual):
                self.__set_error(
                    CompareError(self.__path, ARRAY_SIZE_DIFF, self.__set_error_msg(len(expect), len(actual))))
                return

        current_path = self.__path
        for i in expect:
            self.__path = current_path
            self.__path += "[%d]" % (expect.index(i))

            if isinstance(i, dict):
                key += SUB_OBJ
                self.__compare_obj(key, i, actual[expect.index(i)], is_check_one)
                continue

            if isinstance(i, list):
                self.__path += PATH_ARRAY
                self.__compare_list(key, i, actual[expect.index(i)], is_check_one)
                continue

        pass

    @staticmethod
    def __compare_primitive(expect, actual):
        if expect == Rule.IS_JSON_PRIMITIVE.value or expect == Rule.IGNORE_VALUE.value:
            return True

        if expect != actual:
            if expect == Rule.IS_ANY_INTEGER.value and isinstance(actual, int):
                return True

            if expect == Rule.IS_ANY_FLOAT.value and isinstance(actual, float):
                return True

            if expect == Rule.IS_ANY_STRING.value and isinstance(actual, str):
                return True

            if expect == Rule.IS_ANY_BOOL.value and isinstance(actual, bool):
                return True

            if expect == Rule.IS_JSON_ARRAY.value and isinstance(actual, list):
                return True

            if expect == Rule.IS_TIMESTEMP.value:
                try:
                    datetime.datetime.strptime(actual, '%Y-%m-%d %H:%M:%S')
                    return True
                except ValueError:
                    pass

            if str(expect).startswith(str(Rule.MATCH_REGEX.value)):
                # pattern = re.compile(expect[len(str(Rule.MATCH_REGEX.value)):])
                # return pattern.match(actual) != None
                return re.search(expect[len(str(Rule.MATCH_REGEX.value)):], actual)

            return False
        else:
            return True

    @staticmethod
    def __set_error_msg(expect, actual):
        return "\t\tExpect: %s\n\t\tActual: %s" % (expect, actual) + DEBUG_LINE

    def __set_error(self, compare_error: CompareError):
        self.error_msg += compare_error.__str__()

    @staticmethod
    def __is_primitive(value):
        if isinstance(value, int):
            return True
        if isinstance(value, str):
            return True
        if isinstance(value, bool):
            return True

        return False


if __name__ == '__main__':
    e_data = CompareData(200, expect_test_data, True)
    a_data = CompareData(200, actual_test_data, False)
    print(e_data)
    print(a_data)

    test_comparator = Comparator()
    test_comparator.set_rule(PATH_ROOT, Rule.IGNORE_OBJECT_KEY_MISS_MATCH.value)
    # comparator.set_rule(PATH_ROOT, Rule.IS_JSON_OBJECT.value)

    test_comparator.set_rule("result", Rule.IGNORE_ARRAY_SIZE.value)
    test_comparator.set_rule("result" + SUB_OBJ, Rule.IGNORE_OBJECT_KEY_MISS_MATCH.value)
    # comparator.set_rule("result", Rule.IS_JSON_ARRAY.value)

    test_result = test_comparator.compare(e_data, a_data)
    print(test_result)
