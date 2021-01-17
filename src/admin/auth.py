from admin import admin_blue
from flask import request, jsonify
from util import generate_access_token, login_required

@admin_blue.route('/AdminLogin', methods=('POST','GET'))
def AdminLogin():
    username = request.json.get('username')
    password = request.json.get('password')

    if username and password:
        if username == 'leonAdmin' and password == 'wuhuqifei':
            access_token = generate_access_token(username=username)
            return jsonify({'data': 'ok','token': access_token})
        else:
            return jsonify({'data': 'err'})


@admin_blue.route('/SearchUser', methods=('POST','GET'))
@login_required
def SearchUser():
    username = request.args.get('id')

    print(username=='')
    return "ok"