from common.api.httpUtils.httpUtil import *
from common.api.jsonCompare.compare import CompareData, Comparator


class ApiTestBase(object):
    def __init__(self):
        self.log = BaseLog(ApiTestBase.__name__).log
        self.res = None  # type: ResponseItems

    def do_compare(self, request_items: RequestItems, expect_code: int, expect_json, comparator=None, **kwargs):
        self.log.info("\n" + "=" * 100 + "\n" + request_items.__str__())
        self.res = do_request(request_items, **kwargs)
        self.log.info(self.res)

        if isinstance(expect_json, dict):
            expect = CompareData(expect_code, expect_json, True)
            actual = CompareData(self.res.status, self.res.json, False)
        elif isinstance(expect_json, list):
            expect = CompareDataList(expect_code, expect_json, True)
            actual = CompareDataList(self.res.status, self.res.json, False)
        else:
            raise Exception()

        self.log.info(expect)
        self.log.info(actual)

        if comparator is None:
            result = Comparator().compare(expect, actual)
        else:
            result = comparator.compare(expect, actual)
        self.log.info(result)

        if result.is_same is False:
            raise Exception("Run Fail!")
        else:
            self.log.info("Run Success!")

        import time
        time.sleep(1)
