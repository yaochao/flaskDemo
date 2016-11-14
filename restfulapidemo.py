#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/12

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/demo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': map(make_public_uri, tasks)})

@app.route('/demo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda x: x['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# 自定义404提示为json
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

@app.route('/demo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    if len(tasks) == 0:
        id = 1
    else:
        id = tasks[-1]['id'] + 1
    task = {
        'id': id,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/demo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # task = filter(lambda x: x['id'] == task_id, tasks)
    # print 'task---', task
    # if len(task) == 0:
    #     abort('404')
    # ⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️
    # 这边把错误404写错字符串'404',报的错误是500,'str' object is not callable
    task = filter(lambda x: x['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    task = task[0]
    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['done'] = request.json.get('done', task['done'])
    return jsonify({'task': task})

@app.route('/demo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda x: x['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'task': task[0], 'result': True})

#不直接返回任务的 ids，我们直接返回控制这些任务的完整的 URI，
# 以便客户端可以随时使用这些 URIs。
# 为此，我们可以写一个小的辅助函数生成一个 “公共” 版本任务发送到客户端:
def make_public_uri(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

# 安全认证
@auth.get_password
def get_password(username):
    if username == 'hello':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


if __name__ == '__main__':
    app.debug = True
    app.run()