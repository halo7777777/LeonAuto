from user import user_blue
from flask import request, jsonify
from models import User
from util import generate_access_token, login_required

@user_blue.route('/UserLogin', methods=('POST',))
def UserLogin():
    username = request.json.get('username')
    password = request.json.get('password')
    if username and password:
        user = User.query.filter_by(id=username).first()
        if user is not None and password == user.password:
            access_token = generate_access_token(username=username)

            return jsonify({'data': 'ok', 'token': access_token})
    return jsonify({'data': 'err'})