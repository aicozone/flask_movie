# 视图处理文件
from . import admin
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request,
)
from .forms import LoginForm
from app.models import Admin
from functools import wraps


# 用户登录装饰器
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# 控制面板
@admin.route("/")
@admin_login_required
def index():
    return render_template("admin/index.html")


# 管理员登录
@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误！")
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        return redirect(url_for("admin.index") or request.args.get("next"))
    return render_template("admin/login.html", form=form)


# 管理员登出
@admin.route("/logout")
@admin_login_required
def logout():
    session.pop("admin", None)
    return redirect(url_for('admin.login'))


# 修改密码
@admin.route("/pwd")
@admin_login_required
def pwd():
    return render_template("admin/pwd.html")


# 编辑标签
@admin.route("/tag_add")
@admin_login_required
def tag_add():
    return render_template("admin/tag_add.html")


# 标签列表
@admin.route("/tag_list")
@admin_login_required
def tag_list():
    return render_template("admin/tag_list.html")


# 添加电影
@admin.route("/movie_add")
@admin_login_required
def movie_add():
    return render_template("admin/movie_add.html")


# 电影列表
@admin.route("/movie_list")
@admin_login_required
def movie_list():
    return render_template("admin/movie_list.html")


# 添加预告
@admin.route("/preview_add")
@admin_login_required
def preview_add():
    return render_template("admin/preview_add.html")


# 预告列表
@admin.route("/preview_list")
@admin_login_required
def preview_list():
    return render_template("admin/preview_list.html")


# 会员列表
@admin.route("/user_list")
@admin_login_required
def user_list():
    return render_template("admin/user_list.html")


# 评论列表
@admin.route("/comment_list")
@admin_login_required
def comment_list():
    return render_template("admin/comment_list.html")


# 电影收藏列表
@admin.route("/moviecol_list")
@admin_login_required
def moviecol_list():
    return render_template("admin/moviecol_list.html")


# 操作日志列表
@admin.route("/oplog_list")
@admin_login_required
def oplog_list():
    return render_template("admin/oplog_list.html")


# 管理员登录日志列表
@admin.route("/adminloginlog_list")
@admin_login_required
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")


# 会员登录日志列表
@admin.route("/userloginlog_list")
@admin_login_required
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")


# 添加权限
@admin.route("/auth_add")
@admin_login_required
def auth_add():
    return render_template("admin/auth_add.html")


# 添加权限
@admin.route("/auth_list")
@admin_login_required
def auth_list():
    return render_template("admin/auth_list.html")


# 添加角色
@admin.route("/role_add")
@admin_login_required
def role_add():
    return render_template("admin/role_add.html")


# 角色列表
@admin.route("/role_list")
@admin_login_required
def role_list():
    return render_template("admin/role_list.html")


# 添加角色
@admin.route("/admin_add")
@admin_login_required
def admin_add():
    return render_template("admin/admin_add.html")


# 角色列表
@admin.route("/admin_list")
@admin_login_required
def admin_list():
    return render_template("admin/admin_list.html")
