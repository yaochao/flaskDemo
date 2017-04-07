#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/15
from flask import Flask, request
from flask_restful import Api, Resource, request
import requests

app = Flask(__name__)
api = Api(app)

token_ip138 = 'fd4711d74049c7a98dcaede7f4e17c94'

class GetIP(Resource):
    def get(self):
        # ip
        remote_addr = request.remote_addr
        address = self.ip138(remote_addr)
        # ua
        headers = request.headers.get('User-Agent')
        user_agent = request.user_agent
        print headers

        return {
            'ip': remote_addr,
            'address': address,
        }

    def ip138(self, ip):
        url = 'http://api.ip138.com/query/?datatype=jsonp&ip=' + str(ip)
        response = requests.get(url, headers={'token': token_ip138})
        if response.status_code == 200:
            rst = response.json()
            if rst['ret'] == u'ok':
                return ''.join(rst['data'])

api.add_resource(GetIP, '/ip')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
