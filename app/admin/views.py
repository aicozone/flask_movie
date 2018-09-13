# 视图处理文件
from . import admin

@admin.route("/")
def index():
    return "<h1 style='color:blue'>this is admin</h1>"