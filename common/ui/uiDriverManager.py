# coding = utf-8
from common.ui import *


class UIDriverManager(object):
    def __init__(self):
        self.log = BaseLog(UIDriverManager.__name__).log
        self.__driver = self.__init_driver(DRIVER["type"])  # type: DRIVER["type"]
        if self.__driver is None:
            raise Exception("Driver init failed, Driver is None!")

        self.log.info("<<< init done ")
        self.__windows = {}
        self.__current_window = {}

    def get_driver(self):
        return self.__driver

    def close(self):
        """close WebDriver"""
        self.log.info("close driver: %s", self.__driver)
        if self.__driver is not None:
            self.__driver.quit()

    def __set_basic_web_property(self, driver):
        self.log.info("__WINDOW: max")
        driver.maximize_window()
        self.log.info("__DEFAULT_FIND_ELEMENT_TIMEOUT: %ds", DEFAULT_FIND_ELEMENT_TIMEOUT)
        driver.implicitly_wait(DEFAULT_FIND_ELEMENT_TIMEOUT)
        self.log.info("__DEFAULT_PAGE_LOAD_TIMEOUT: %ds", DEFAULT_PAGE_LOAD_TIMEOUT)
        driver.set_page_load_timeout(DEFAULT_PAGE_LOAD_TIMEOUT)
        return driver

    def __init_driver(self, driver_type):
        self.log.info(">>> init driver ")
        if driver_type == webdriver.Chrome:
            self.log.info("Create Chrome Driver...")
            options = webdriver.ChromeOptions()

            self.log.info("Allow \"Trying to download multiple files\"")
            prefs = {
                'profile.content_settings.exceptions.automatic_downloads.*.setting': 1,  # 允许自动下载多个文件
                "profile.default_content_settings.popups": 0,  # 下载不弹框
                "download.directory_upgrade": True,
                "download.default_directory": DEFAULT_DOWNLOAD_PATH,  # 指定下载路径
            }
            options.add_experimental_option("prefs", prefs)

            self.log.info("Set disable-infobars")
            options.add_argument('disable-infobars')
            driver = webdriver.Chrome(chrome_options=options)  # type: webdriver.Chrome
            return self.__set_basic_web_property(driver)
        elif driver_type == webdriver.Firefox:
            self.log.info("Create FireFox Driver...")
            driver = webdriver.Firefox(log_path=GECKO_DRIVER_LOG_PATH)  # type: webdriver.Firefox
            return self.__set_basic_web_property(driver)
        else:
            raise Exception("unimplemented driver type")

    def add_window(self, window_name: str):
        windows = self.__driver.window_handles  # type:list
        if len(windows) - len(self.__windows) == 1:
            for i in windows:
                if i not in self.__windows.values():
                    self.__windows[window_name] = i
        else:
            raise Exception("Windows must add one by one")

        if len(self.__windows) == 1:
            self.__current_window.clear()
            self.__current_window[window_name] = self.__windows[window_name]

    def switch_to_window(self, window_name: str):
        self.__current_window.clear()
        self.__current_window[window_name] = self.__windows[window_name]
        return self.__driver.switch_to_window(self.__windows[window_name])

    def current_window(self):
        return self.__current_window


if __name__ == "__main__":
    manager = UIDriverManager()
    test_driver = manager.get_driver()

    test_driver.get("https://www.baidu.com")

    time.sleep(1)

    manager.close()
