# coding; utf-8
from selenium.webdriver.common.by import By


class Page(object):
    id = By.ID
    xpath = By.XPATH
    className = By.CLASS_NAME
    tag = By.TAG_NAME
    css = By.CSS_SELECTOR
    link = By.LINK_TEXT
    name = By.NAME
    pLink = By.PARTIAL_LINK_TEXT
