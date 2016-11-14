#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/15

from flask import Flask
from flask_restful import Resource, reqparse, Api, abort
from sqldb_demo import MySQLDemo


app = Flask(__name__)
api = Api(app)

students = {}
req_parse = reqparse.RequestParser()
req_parse.add_argument('name')


def if_not_exists(student_id):
    if student_id not in students:
        abort(404, message='{}  is not exists'.format(student_id))


class Demo(Resource):

    def get(self, student_id):
        if_not_exists(student_id)
        return students[student_id]

    def post(self, student_id):
        args = req_parse.parse_args()
        if student_id in students:
            abort(400, message='%s already exists, use PUT method to update.' % student_id)
        students[student_id] = {'name': args['name']}
        return students[student_id], 201

    def put(self, student_id):
        args = req_parse.parse_args()
        if_not_exists(student_id)
        students[student_id] = {'name': args['name']}
        return students[student_id], 201

    def delete(self, student_id):
        if_not_exists(student_id)
        del students[student_id]
        return '', 204

# 转换从数据库查询出来的结果为符合标准json格式类型的数据(还不是json,其实还是字典和数组)
def format_result(rets):
    rets2 = []
    for ret in list(rets):
        keys = ['id', 'name', 'brand', 'md5', 'url', 'maincolor']
        re = dict(zip(keys, list(ret)))
        rets2.append(re)
    return rets2


class Get_With_Brand(Resource):

    def get(self, brand):
        mysqldemo = MySQLDemo()
        rets = mysqldemo.select_with_name(brand=brand)
        rets2 = format_result(rets)
        return {'data': rets2}


class Get_With_Name(Resource):

    def get(self, name):
        mysqldemo = MySQLDemo()
        rets = mysqldemo.select_with_name(name=name)
        rets2 = format_result(rets)
        return {'data': rets2}


class Get_With_Maincolor(Resource):

    def get(self, maincolor):
        mysqldemo = MySQLDemo()
        rets = mysqldemo.select_with_name(maincolor=maincolor)
        rets2 = format_result(rets)
        return {'data': rets2}


api.add_resource(Get_With_Brand, '/brand=<string:brand>')
api.add_resource(Get_With_Name, '/name=<string:name>')
api.add_resource(Get_With_Maincolor, '/maincolor=<string:maincolor>')


if __name__ == '__main__':
    app.run(debug=True)