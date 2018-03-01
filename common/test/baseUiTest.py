from common.test import *

from common.ui.uiDriverManager import *


def exception_handler(is_open=False):
    def foo(func):
        def bar(*args, **kwargs):
            if is_open:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    for i in args:
                        if isinstance(i, UITestBase):
                            i.log.exception(e)
                    time.sleep(1)
                    input("input any key to continue:")
                    raise e
            else:
                return func(*args, **kwargs)

        return bar

    return foo


class UITestBase(unittest.TestCase):
    def setUp(self):
        self.manager = UIDriverManager()
        self.driver = self.manager.get_driver()  # type: DRIVER["type"]
        self.log = BaseLog(UITestBase.__name__).log

    def tearDown(self):
        self.manager.close()
