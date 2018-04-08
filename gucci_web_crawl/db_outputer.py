# -*- coding: utf-8 -*-
import pyodbc

from gucci_web_crawl.db_helper import DbHelper


class DbOutputer(object):
    def __init__(self):
        self.conn = DbHelper.conn
        self.crawledUrl_tb = "CrawledUrl"
        self.product_tb = "Product"
        self.country_code = "USD"

    # def collect_data(self, data):
    #     if data is None:
    #         return
    #     self.datas.append(data)

    def insert_data_to_db(self, data):
        if data is None:
            return

        self.insert_crawled_url_to_db(data['url'])

        # conn = DbHelper.connect_msdb()
        cursor = self.conn.cursor()

        cateId = 'null'
        temp = DbHelper.get_category_id(data['category'])
        if temp is not None:
            cateId = temp

        insertContentSql = "IF NOT EXISTS(SELECT * FROM {0} WHERE Code = '{1}' ) " \
                           "BEGIN " \
                           "INSERT INTO {0} (Code, Name, CategoryId, {2}) " \
                           "VALUES ('{1}', '{3}', {4}, {5}) " \
                           "END;"\
            .format(self.product_tb, data['code'], self.country_code,
                    data['name'].encode("utf-8").replace("'", "\'\'"),
                    cateId, float(data['price']))
        # print data['price'], float(data['price'])

        cursor.execute(insertContentSql.decode("utf-8"))
        self.conn.commit()
        # self.conn.close()

    def insert_crawled_url_to_db(self, url):
        if url is None:
            return
        # conn = DbHelper.connect_msdb()
        cursor = self.conn.cursor()
        insertContentSql = "IF NOT EXISTS(SELECT * FROM {0} WHERE Url = '{1}') " \
                           "BEGIN " \
                           "INSERT INTO {0} (Url) VALUES ('{1}') " \
                           "END;"\
            .format(self.crawledUrl_tb, url)

        cursor.execute(insertContentSql)
        self.conn.commit()
        # conn.close()

    def close_db_connection(self):
        # self.conn.cursor.close()
        self.conn.close()
        # pass
