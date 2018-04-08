# -*- coding: utf-8 -*-
import traceback

from gucci_web_crawl import url_manager, html_downloader, html_parser, html_outputer, db_outputer


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        # self.outputer = html_outputer.HtmlOutputer()
        self.outputer = db_outputer.DbOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d : %s' % (count, new_url)
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.insert_data_to_db(new_data)

                count = count + 1

            except Exception, Argument:
                # self.outputer.close_db_connection()
                print Argument
                print traceback.format_exc()
                # return

        self.outputer.close_db_connection()


if __name__ == "__main__":
    root_url = "https://www.gucci.com/us/en/"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
