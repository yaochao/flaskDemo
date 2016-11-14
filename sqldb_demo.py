#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/15

import MySQLdb

class MySQLDemo(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='fashionshow')
        self.corsur = self.conn.cursor()

    def select_with_name(self, name='', brand='', maincolor=''):
        sql = ''
        if name:
            if brand:
                if maincolor:
                    sql = 'select * from vogue where name="%s", brand="%s", maincolor="%s"' % (name, brand, maincolor)
                else:
                    sql = 'select * from vogue where name="%s", brand="%s"' % (name, brand)
            else:
                if maincolor:
                    sql = 'select * from vogue where name="%s", maincolor="%s"' % (name, maincolor)
                else:
                    sql = 'select * from vogue where name="%s"' % name
        else:
            if brand:
                if maincolor:
                    sql = 'select * from vogue where brand="%s", maincolor="%s"' % (brand, maincolor)
                else:
                    sql = 'select * from vogue where brand="%s"' % brand
            else:
                if maincolor:
                    sql = 'select * from vogue where maincolor="%s"' % maincolor
        try:
            print sql
            self.corsur.execute(sql)
            rst = self.corsur.fetchall()
            return rst
        except Exception as e:
            print str(e)
        finally:
            self.corsur.close()
            self.conn.close()

