from admin import admin_blue
from flask import request, jsonify
import models
from util import generate_access_token, login_required
from app import db

@admin_blue.route('/AdminLogin', methods=['POST','GET'])
def AdminLogin():
    username = request.json.get('username')
    password = request.json.get('password')

    if username and password:
        if username == 'leonAdmin' and password == 'wuhuqifei':
            access_token = generate_access_token(username=username)
            return jsonify({'errno': 0, 'errmsg': 'ok', 'token': access_token})
        else:
            return jsonify({'errno':120, 'errmsg': 'username_password_mismatch'}), '400 ERR'


@admin_blue.route('/SearchUser', methods=['POST','GET'])
@login_required
def SearchUser():
    username = request.values.get('id')
    if username == '':
        users = models.User.query.all()
    else:
        users = models.User.query.filter_by(id=username).all()
    UserList = []
    for user in users:
        UserList.append(user.as_dict())
    return jsonify({'errno': 0, 'errmsg': 'ok', 'UserList': UserList})


@admin_blue.route('/UserNew', methods=['POST','GET'])
@login_required
def UserNew():
    username = request.json.get('id')
    password = request.json.get('password')
    name = request.json.get('name')

    user_exist = models.User.query.filter_by(id=username).first()

    if user_exist != None:
        return jsonify({'errno': 126, 'errmsg': 'user_existed'}), '400 ERR'
    else:
        new_user = models.User(id=username, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'errno': 0, 'errmsg': 'ok'})


@admin_blue.route('/UserEdit', methods=['PUT'])
@login_required
def UserEdit():
    username = request.json.get('id')
    password = request.json.get('password')
    name = request.json.get('name')

    user_exist = models.User.query.filter_by(id=username).first()
    if user_exist == None:
        return jsonify({'errno': 121, 'errmsg': 'invalid_user'}), '400 ERR'
    else:
        user_exist.password = password
        user_exist.name = name
        db.session.add(user_exist)
        db.session.commit()
        return jsonify({'errno': 0, 'errmsg': 'ok'})


@admin_blue.route('/UserDelete', methods=['DELETE'])
@login_required
def UserDelete():
    username = request.data.decode('utf-8')
    print(username)
    user_delete = models.User.query.filter_by(id=username).first()
    if user_delete == None:
        return jsonify({'errno': 121, 'errmsg': 'invalid_user'}), '400 ERR'
    else:
        db.session.delete(user_delete)
        db.session.commit()
        return jsonify({'errno': 0, 'errmsg': 'ok'})