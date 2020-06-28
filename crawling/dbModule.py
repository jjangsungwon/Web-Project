# file name : dbModule.py
# pwd : /project_name/app/module/dbModule.py

import pymysql


class Database():
    def __init__(self):
        self.db = pymysql.connect(host='107.21.40.27',
                                  user='{KJY}',
                                  password='{KJY}',
                                  db='testDB',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
