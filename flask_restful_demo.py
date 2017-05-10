#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/15
import json

from flask import Flask, request, abort
from flask_restful import Resource, Api
from webspiders import WanfangSpider, It199Spider


app = Flask(__name__)
api = Api(app)
todos = {}


class HelloWorld(Resource):

    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def post(self, todo_id):
        print request.json
        todos[todo_id] = request.json['data']
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        item = todos[todo_id]
        if not item:
            abort(404)
        item[todo_id] = request.json[todo_id]
        return item

class Wanfang(Resource):
    def get(self, keyword):
        result = WanfangSpider.crawl_with_keyword(keyword)
        if result:
            return {'msg': 'ok', 'data': result}
        else:
            return {'msg': 'error', 'data': {}}

class It199(Resource):
    def get(self, keyword):
        result = It199Spider.crawl_with_keyword(keyword)
        if result:
            return {'msg': 'ok', 'data': result}
        else:
            return {'msg': 'error', 'data': {}}

class Content(Resource):
    def get(self, url):
        result = It199Spider.get_content(url)
        if result:
            return result
        else:
            return {'msg': 'error', 'data': {}}


api.add_resource(It199, '/199it/<string:keyword>')
api.add_resource(Wanfang, '/wanfangdata/<string:keyword>')
api.add_resource(Content, '/getcontent/<string:url>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)