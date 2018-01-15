from common.interface.httpUtils.httpMethod import HttpMethod


class BaseRequest(object):
    def __init__(self, url: str, method: HttpMethod):
        self.url = url
        self.method = method
