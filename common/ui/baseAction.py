# coding; utf-8
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from common.ui import *


def check_point(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        for i in args:
            if isinstance(i, BaseAction):
                i.check_log()
                break
        return result

    return wrapper


class BaseAction(object):
    def __init__(self, selenium_driver):
        self.driver = selenium_driver  # type: DRIVER["type"]
        self.log = BaseLog(BaseAction.__name__).log
        self.browser_log_ignores = []

    @check_point
    def open(self, url):
        self.log.info("open url: %s", url)
        self.driver.get(url)

    def sleep(self, sleep_time=0.5):
        self.log.info("sleep: %.1fs", sleep_time)
        time.sleep(sleep_time)

    def find_element(self, *loc):
        self.log.info("find element by: " + str(loc))
        return self.driver.find_element(*loc)

    def find_elements(self, *loc):
        self.log.info("find elements by: " + str(loc))
        return self.driver.find_elements(*loc)

    @check_point
    def script(self, src):
        self.log.info("execute script: %s", src)
        return self.driver.execute_script(src)

    @check_point
    def click(self, *loc, sleep=True):
        element = self.find_element(*loc)
        self.log.info("click element: %s", loc)
        element.click()
        if sleep:
            self.sleep()

    @check_point
    def send_keys(self, *loc, value, click_first=False, clear_first=False):
        if click_first:
            self.find_element(*loc).click()
            self.sleep()
        if clear_first:
            self.find_element(*loc).clear()

        element = self.find_element(*loc)
        self.log.info("send value: %s to element: %s", value, loc)
        element.send_keys(value)

    def chains(self):
        from selenium.webdriver.common.action_chains import ActionChains
        return ActionChains(self.driver)

    def wait_element_visible(self, timeout, loc):
        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(loc))

    @check_point
    def get_only_one_visible_element_of_list(self, *loc):
        elements = self.find_elements(*loc)
        if elements.__len__() == 0:
            raise Exception("elements list: len is 0")

        tar = []

        for i in elements:  # type: WebElement
            if i.is_displayed():
                tar.append(i)

        if tar.__len__() == 0:
            raise Exception("No Displayed Element")
        elif tar.__len__() == 1:
            return tar[0]
        else:
            raise Exception("Multiple Displayed Element of list:%s" % tar)

    def check_log(self):
        for i in self.driver.get_log("browser"):  # type:dict
            if i.get("level") == "SEVERE":
                flag = True
                for j in self.browser_log_ignores:  # type: str
                    if j in i.get("message"):
                        flag = False
                        break
                if flag:
                    raise Exception("Browser Console Error: %s" % i)
            elif i.get("level") == "WARNING":
                self.log.warning("Browser Console Warning: %s" % i)
            else:
                self.log.info("Console Msg: %s" % i)
