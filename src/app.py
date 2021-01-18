from flask import Flask
from flask_cors import CORS
from admin import admin_blue
from user import user_blue
from flask_sqlalchemy import SQLAlchemy
import pymysql

__author__ = 'leon'

app = Flask(__name__)

 # 全局跨域配置
CORS(app, oringins=r'*')

# 注册蓝图
app.register_blueprint(admin_blue)
app.register_blueprint(user_blue)

# 各项插件配置
app.config['SECRET_KEY'] = 'leon'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'leonauto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSWORD, HOST, PORT, DATABASE
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy()
db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True, port=9090)