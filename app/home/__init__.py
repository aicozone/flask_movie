# 前台模块
from flask import Blueprint


# 定义蓝图
home = Blueprint("home", __name__)
from . import views