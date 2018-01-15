from common.test import *

from common.ui.uiDriverManager import *


class UITestBase(unittest.TestCase):
    def setUp(self):
        self.manager = UIDriverManager()
        self.driver = self.manager.get_driver()  # type: DRIVER["type"]
        self.log = BaseLog(UITestBase.__name__).log

    def tearDown(self):
        self.manager.close(self.driver)
