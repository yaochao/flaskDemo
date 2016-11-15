#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/11/9

import json
import sqlite3
import time

import MySQLdb

from webspiders_copy import It199Spider


# connection = MySQLdb.connect(host='192.168.31.7', port=3306, user='root', passwd='dp12345678', db='dataparkcn')


def go():
    # sqlite3
    connection2 = sqlite3.connect('blacknamelist_199it.data')
    cursor2 = connection2.cursor()
    # mysql
    connection = MySQLdb.connect(host='192.168.39.25', port=3306, user='root', passwd='7Rgag9o868YigP2E',
                                 db='dataparkcn')
    cursor = connection.cursor()
    cursor.execute('select r_tag, r_id from new_reports')
    results = cursor.fetchall()
    for index, result in enumerate(results):
        r_id = result[1]
        cursor.execute('select relatedOutReports from new_reports WHERE r_id=%s' % r_id)
        rs = cursor.fetchone()
        relatedOutReports = rs[0]
        result = result[0]
        if not result:
            continue
        if relatedOutReports:
            continue
        cursor2.execute('CREATE TABLE IF NOT EXISTS BLACKNAMELIST_199IT (id INT)')
        connection2.commit()
        cursor2.execute('SELECT * FROM BLACKNAMELIST_199IT WHERE id=%s' % r_id)
        rs = cursor2.fetchall()
        if rs:
            continue
        print '1', type(result)
        result = result.strip()
        result = result.split(',')[0] if result.split(',') else result
        # if '，' in result:
        #     result = result.split('，')[0] if result.split('，') else result
        # if ' ' in result:
        #     result = result.split()[0] if result.split() else result
        print '2', result
        try:
            jsonstr = It199Spider.crawl_with_keyword(result)
            if jsonstr == 'ggsimida':
                cursor2.execute('INSERT INTO BLACKNAMELIST_199IT (id) VALUES (%s)' % r_id)
                connection2.commit()
            else:
                if jsonstr:
                    jsonstr = {'message': 'ok', 'data': jsonstr}
                    sql = 'update new_reports set relatedOutReports="' + json.dumps(jsonstr, encoding='utf-8').replace('\\',
                                                                                                                 '\\\\').replace(
                        '"', '\\"') + '"WHERE r_id=' + str(r_id)
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
    main()


def main():
    count = 0
    while True:
        print('199it next time crawl after--- %ss' % str(3 - count))
        time.sleep(1)
        count += 1
        if count == 3:
            go()
            return


if __name__ == '__main__':
    main()
