from common.util.jsonFormat import *


class CompareData(object):
    def __init__(self, code: int, data: dict, is_expect):
        self.code = code
        self.data = data
        self.is_expect = is_expect

    def __str__(self):
        if self.is_expect:
            return "Expect:\n\t%s data: %s" % (self.code, json_format(self.data))
        return "Actual:\n\t%s data: %s" % (self.code, json_format(self.data))


class CompareDataList(object):
    def __init__(self, code: int, data: list, is_expect):
        self.code = code
        for i in data:
            if isinstance(i, dict) is False:
                raise Exception("param data must be 'List[dict]'")

        self.data = data
        self.is_expect = is_expect

    def __str__(self):
        if self.is_expect:
            return "Expect:\n\t%s data: %s" % (self.code, json_format(self.data))
        return "Actual:\n\t%s data: %s" % (self.code, json_format(self.data))
