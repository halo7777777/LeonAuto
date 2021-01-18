from user import user_blue
from flask import request, jsonify
import models
from util import generate_access_token, login_required

@user_blue.route('/UserLogin', methods=('POST',))
def UserLogin():
    username = request.json.get('username')
    password = request.json.get('password')
    if username and password:
        user = models.User.query.filter_by(id=username).first()
        if user is not None and password == user.password:
            access_token = generate_access_token(username=username)

            return jsonify({'errno': 0, 'errmsg': 'ok', 'token': access_token})
    return jsonify({'errno': 120, 'errmsg': 'username_password_mismatch'}), '400 ERR'