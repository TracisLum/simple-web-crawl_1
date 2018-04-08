# -*- coding: utf-8 -*-
import re
import urlparse
import urllib2


from bs4 import BeautifulSoup

from gucci_web_crawl.db_helper import DbHelper
from gucci_web_crawl.url_manager import UrlManager


class HtmlParser(object):
    def __init__(self):
        self.re_product_code = [re.compile(r'-p-(.+)\?'), re.compile(r'-p-(.+)')]
        # ?categoryPath=Men/Mens-Shoes/Mens-Monk-Straps
        # self.re_category = re.compile(r'categoryPath=(.+)/(.+)/(.+)')
        self.base_url = "https://www.gucci.com"
        self.page_url = "https://www.gucci.com"
        self.product_code = None

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        self.page_url = page_url

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _is_product_page(self, page_url):
        if re.match('https://www.gucci.com/us/en/', page_url) is not None and "/us/en/pr/" in page_url:
            return True
        return False

    def _get_product_code_from_page_url(self, page_url):
        if self._is_product_page(page_url):
            product_code = re.search(self.re_product_code[0], page_url)
            if (product_code is not None):
                return product_code.group(1)
            else:
                return re.search(self.re_product_code[1], page_url).group(1)
        return None

    def _get_new_urls(self, soup):
        new_urls = set()
        # /us/en/pr
        links = soup.find_all('a', href=re.compile(r"(^/us/en/)"))
        for link in links:
            new_url = urllib2.unquote(link['href'].encode("utf-8"))
            new_full_url = urlparse.urljoin(self.base_url, new_url)

            product_code = self._get_product_code_from_page_url(new_full_url)
            if product_code is not None:
                if DbHelper.is_product_code_in_db(product_code):
                    continue
            if new_full_url not in UrlManager.old_urls:
                new_urls.add(new_full_url)

        return new_urls

    def _get_new_data(self, page_url, soup):
        if not self._is_product_page(page_url):
            return None

        res_data = {}

        # url
        res_data['url'] = page_url

        product_code = re.search(self.re_product_code[0], page_url)
        if(product_code is not None):
            res_data['code'] = product_code.group(1)
        else:
            res_data['code'] = re.search(self.re_product_code[1], page_url).group(1)

        # <h1 class="product-name product-detail-product-name">RE(BELLE) medium top handle bag</h1>
        title_node = soup.find('h1', class_="product-detail-product-name")
        res_data['name'] = title_node.get_text()

        # <div class="product-price product-detail-price">
        #          <div class="price-column product-detail-price-column">
        #                 <span id="markedDown_full_Price" class="price">$ 2,600</span>
        summary_node = soup.find('div', class_="product-detail-price").find('span', class_="price")
        res_data['price'] = summary_node.get_text()[2:].replace(',', '')

        res_data['category'] = self._get_product_category_from_url(page_url)

        # if re.search(self.re_category, page_url) is None:
        #     cats_search_len = 0
        # else:
        #     cats_search_len = len(re.search(self.re_category, page_url).groups())
        # for inx in range(1, 4):
        #     if inx <= cats_search_len:
        #         res_data['cat_{0}'.format(inx)] = re.search(self.re_category, page_url).group(inx)
        #     else:
        #         res_data['cat_{0}'.format(inx)] = 'null'

        return res_data

    def _get_product_category_from_url(self, page_url):
        search_result = re.search(r'categoryPath=(.+)', page_url)
        if search_result is None:
            return None
        else:
            cates = search_result.group(1).split('/')
            level = 1
            parentCateName = ''
            for cateName in cates:
                DbHelper.add_category_to_db(cateName, level, parentCateName)
                parentCateName = cateName
                level = level + 1
            return parentCateName
