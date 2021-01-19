from flask import Flask
from flask_cors import CORS
from admin import admin_blue
from user import user_blue
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_apscheduler import APScheduler
import platform, atexit

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
db = SQLAlchemy(app)
db.init_app(app)

#APscheduler配置任务
scheduler = APScheduler()
app.config.update(
    {
        "SCHEDULER_API_ENABLED": True,
        "SCHEDULER_TIMEZONE": "Asia/Shanghai",
        "JOBS": 
        [
            {
                "id": "card",
                "func": "admin:tec.card",
                "trigger": "interval",
                "seconds": 5
            }
        ]
    }
)

# 保证apschedule只执行一次
if platform.system() != 'Windows':
    fcntl = __import__("fcntl")
    f = open('scheduler.lock', 'wb')
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler.init_app(app)
        scheduler.start()
        app.logger.debug('Scheduler Started,---------------')
    except:
        pass

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    atexit.register(unlock)
else:
    msvcrt = __import__('msvcrt')
    f = open('scheduler.lock', 'wb')
    try:
        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        scheduler.init_app(app)
        scheduler.start()
        app.logger.debug('Scheduler Started,----------------')
    except:
        pass

    def _unlock_file():
        try:
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass

    atexit.register(_unlock_file)


if __name__ == '__main__':
    app.run(debug=False, port=9090)