from datetime import datetime, timedelta
from flask import request, jsonify, session
import jwt
from functools import wraps


key = "leonwuhuqifei" # secret私钥,可通过配置文件导入

def generate_access_token(username: str = "", algorithm: str = 'HS256', exp: float = 24):
    """
    生成access_token
    :param username: 用户名(自定义部分)
    :param algorithm: 加密算法
    :param exp: 过期时间
    :return:token
    """

    now = datetime.utcnow()
    exp_datetime = now + timedelta(hours=exp)
    access_payload = {
        'exp': exp_datetime,
        'flag': 0,   #标识是否为一次性token，0是，1不是
        'iat': now,   # 开始时间
        'iss': 'leon',   # 签名
        'username': username   #用户名(自定义部分)
    }
    access_token = jwt.encode(access_payload, key, algorithm=algorithm)
    return access_token


def decode_auth_token(token: str):
    """
    解密token
    :param token:token字符串
    :return:
    """
    try:
        payload = jwt.decode(token, key=key, algorithms='HS256')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidSignatureError):
        return ""
    else:
        return payload


def identify(auth_header: str):
    """
    用户鉴权
    """

    if auth_header:
        payload = decode_auth_token(auth_header)
        if not payload:
            return False
        if "username" in payload and "flag" in payload:
            if payload["flag"] == 0:
                return payload["username"]
            else:
                return False
    return False


def login_required(f):
    """
    登录保护，验证用户是否登录
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", default=None)
        if not token:
            return jsonify({'errno':118, 'errmsg': 'invalid_authorization_code'}), '400 ERR'
        username = identify(token)
        if not username:
            return jsonify({'errno':118, 'errmsg': 'invalid_authorization_code'}), '400 ERR'
        return f(*args, **kwargs)
    return wrapper

    # return 响应体, 状态码, 响应头