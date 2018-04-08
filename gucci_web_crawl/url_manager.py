# -*- coding: utf-8 -*-
class UrlManager(object):
    old_urls = set()

    def __init__(self):
        self.new_urls = set()
        # self.old_urls = set()

    @staticmethod
    def has_url(url):
        if(url in UrlManager.old_urls):
            return True
        return False

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in UrlManager.old_urls:
            self.new_urls.add(url)
            # print url

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        UrlManager.old_urls.add(new_url)
        return new_url
