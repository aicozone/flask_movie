# 视图处理文件
from . import home

# 调用蓝图
@home.route("/")
def index():
    return "<h1 style='color:red'>this is home</h1>"