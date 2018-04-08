import pyodbc


class DbHelper(object):
    conn = pyodbc.connect(
            r'DRIVER={ODBC Driver 11 for SQL Server};'
            r'SERVER=LUM;'
            r'DATABASE=GucciPriceIntelligence;'
            r'UID=GucciPriceIntelligence;'
            r'PWD=GucciPriceIntelligence1234'
        )

    product_tb = "Product"
    product_code_tb = "Code"
    country_code = "USD"

    category_tb = "ProductCategory"

    def __init__(self):
        self.conn = self.connect_msdb()

    @staticmethod
    def connect_msdb():
        conn = pyodbc.connect(
            r'DRIVER={ODBC Driver 11 for SQL Server};'
            r'SERVER=LUM;'
            r'DATABASE=GucciPriceIntelligence;'
            r'UID=GucciPriceIntelligence;'
            r'PWD=GucciPriceIntelligence1234'
        )
        return conn

    @staticmethod
    def is_product_code_in_db(code):
        if code is None:
            return False

        flag = False
        # conn = DbHelper.connect_msdb()
        cursor = DbHelper.conn.cursor()
        query_str = "SELECT * FROM {0} WHERE {1} = '{2}';".format(DbHelper.product_tb, DbHelper.product_code_tb, code)
        cursor.execute(query_str)

        if cursor.fetchone() is not None:
            flag = True

        # DbHelper.conn.close()
        return flag

    @staticmethod
    def add_category_to_db(cateName, level, parentCateName):
        if cateName is None:
            return
        # conn = DbHelper.connect_msdb()
        cursor = DbHelper.conn.cursor()
        query_str = "IF NOT EXISTS (SELECT * FROM {0} WHERE Name = '{1}')" \
                    "INSERT INTO {0} (Name, CatLevel, ParentCateId) " \
                    "VALUES ('{1}', {2}, (SELECT Id FROM {0} b WHERE b.Name = '{3}'));"\
            .format(DbHelper.category_tb, cateName, level, parentCateName)
        cursor.execute(query_str)

        DbHelper.conn.commit()
        # DbHelper.conn.close()

    @staticmethod
    def get_category_id(cateName):
        if cateName is None:
            return None
        # conn = DbHelper.connect_msdb()
        cursor = DbHelper.conn.cursor()
        query_str = "SELECT Id FROM {0} WHERE Name = '{1}'" \
            .format(DbHelper.category_tb, cateName)
        cursor.execute(query_str)

        cateId = cursor.fetchone()[0]
        # DbHelper.conn.close()

        return cateId
