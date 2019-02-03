# 使用动态UA
from fake_useragent import UserAgent


class UserAgentDownloadMiddleware(object):
    def process_request(self, request, spider):
        request.headers.setdefault(b'User-Agent', UserAgent().random)
