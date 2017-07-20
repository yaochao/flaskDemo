#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/11/9

import json

import MySQLdb
import sqlite3
import time
from webspiders_copy import WanfangSpider
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# connection = MySQLdb.connect(host='192.168.31.7', port=3306, user='root', passwd='dp12345678', db='dataparkcn')


def go():

    connection2 = sqlite3.connect('blacknamelist_wanfang.data')
    cursor2 = connection2.cursor()

    connection = MySQLdb.connect(host='192.168.39.25', port=3306, user='root', passwd='7Rgag9o868YigP2E',
                                 db='dataparkcn', charset='utf8')
    cursor = connection.cursor()
    cursor.execute('select r_tag, r_id from new_reports')
    results = cursor.fetchall()
    for index, result in enumerate(results):
        r_id = result[1]
        cursor.execute('select expertInfos from new_reports WHERE r_id=%s' % r_id)
        rs = cursor.fetchone()
        expertInfos = rs[0]
        result = result[0]
        if not result:
            continue
        if expertInfos:
            continue
        cursor2.execute('CREATE TABLE IF NOT EXISTS BLACKNAMELIST_WANFANG (id INT)')
        connection2.commit()
        cursor2.execute('SELECT * FROM BLACKNAMELIST_WANFANG WHERE id=%s' % r_id)
        rs = cursor2.fetchall()
        if rs:
            continue

        result = result.strip()
        result = result.split(u',')[0] if result.split(u',') else result
        if u'，' in result:
            result = result.split(u'，')[0] if result.split(u'，') else result
        if u' ' in result:
            result = result.split()[0] if result.split() else result
        # print result
        try:
            jsonstr = WanfangSpider.crawl_with_keyword(result.encode('utf-8'))
            if jsonstr == 'ggsimida':
                cursor2.execute('INSERT INTO BLACKNAMELIST_WANFANG (id) VALUES (%s)' % r_id)
                connection2.commit()
            else:
                if jsonstr:
                    jsonstr = {'message': 'ok', 'data': jsonstr}
                    sql = 'update new_reports set expertInfos="' + json.dumps(jsonstr, encoding='utf-8').replace('\\',
                                                                                                                 '\\\\').replace(
                        '"', '\\"') + '" WHERE r_id=' + str(r_id)
                    # sql = sql.decode('unicode_escape')
                    print sql
                    cursor.execute(sql)
                    connection.commit()
        except Exception as e:
            print e, index, result
    cursor.close()
    connection.close()
    cursor2.close()
    connection2.close()
    print('crawl complete!')


if __name__ == '__main__':
    go()