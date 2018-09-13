# 后台模块
from flask import Blueprint

# 定义蓝图
admin = Blueprint("admin", __name__)
from . import views