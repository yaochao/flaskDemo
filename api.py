#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/15
import requests
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

results = []


class GetIP(Resource):
    def get(self):
        return results, 200


def get_ips():
    url = 'http://api.zdaye.com/?api=201609221423569186&sleep=1%C3%EB%C4%DA&gb=2&https=%D6%A7%B3%D6&ct=50'
    response = requests.get(url=url)
    if response.status_code == 200:
        if not response.content.startswith('<bad>'):
            ips = response.content.split('\r\n')
            return ips


def check(proxy):
    import urllib2
    url = "https://www.baidu.com/js/bdsug.js"
    proxy_handler = urllib2.ProxyHandler({'https': "https://" + proxy})
    opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
    try:
        response = opener.open(url, timeout=3)
        return response.code == 200
    except Exception:
        return False


def main():
    ips = get_ips()
    for ip in ips:
        if check(ip):
            results.append(ip)
            print ip


api.add_resource(GetIP, '/ip')

if __name__ == '__main__':
    # app.run(debug=True)
    main()