#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/12

from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index'

# 自定义404提示为json
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

@app.route('/hello')
def hello():
    return 'hello world'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post_id(post_id):
    return '%d' % post_id


if __name__ == '__main__':
    app.run(debug=True)