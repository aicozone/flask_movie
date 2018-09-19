# 视图处理文件
from . import admin
from flask import render_template
from flask import redirect
from flask import url_for


# 控制面板
@admin.route("/")
def index():
    return render_template("admin/index.html")


# 管理员登录
@admin.route("/login")
def login():
    return render_template("admin/login.html")


# 管理员登出
@admin.route("/logout")
def logout():
    return redirect(url_for('admin.login'))


# 修改密码
@admin.route("/pwd")
def pwd():
    return render_template("admin/pwd.html")


# 编辑标签
@admin.route("/tag_add")
def tag_add():
    return render_template("admin/tag_add.html")


# 标签列表
@admin.route("/tag_list")
def tag_list():
    return render_template("admin/tag_list.html")


# 添加电影
@admin.route("/movie_add")
def movie_add():
    return render_template("admin/movie_add.html")


# 电影列表
@admin.route("/movie_list")
def movie_list():
    return render_template("admin/movie_list.html")


# 添加预告
@admin.route("/preview_add")
def preview_add():
    return render_template("admin/preview_add.html")


# 预告列表
@admin.route("/preview_list")
def preview_list():
    return render_template("admin/preview_list.html")


# 会员列表
@admin.route("/user_list")
def user_list():
    return render_template("admin/user_list.html")


# 评论列表
@admin.route("/comment_list")
def comment_list():
    return render_template("admin/comment_list.html")


# 电影收藏列表
@admin.route("/moviecol_list")
def moviecol_list():
    return render_template("admin/moviecol_list.html")


# 操作日志列表
@admin.route("/oplog_list")
def oplog_list():
    return render_template("admin/oplog_list.html")


# 管理员登录日志列表
@admin.route("/adminloginlog_list")
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")


# 会员登录日志列表
@admin.route("/userloginlog_list")
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")


# 添加权限
@admin.route("/auth_add")
def auth_add():
    return render_template("admin/auth_add.html")


# 添加权限
@admin.route("/auth_list")
def auth_list():
    return render_template("admin/auth_list.html")


# 添加角色
@admin.route("/role_add")
def role_add():
    return render_template("admin/role_add.html")


# 角色列表
@admin.route("/role_list")
def role_list():
    return render_template("admin/role_list.html")


# 添加角色
@admin.route("/admin_add")
def admin_add():
    return render_template("admin/admin_add.html")


# 角色列表
@admin.route("/admin_list")
def admin_list():
    return render_template("admin/admin_list.html")