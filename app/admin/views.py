# 视图处理文件， 包含管理员的登录面板，标签管理，电影管理，预告管理，会员管理，评论收藏管理，密码修改，日志管理
from . import admin
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request,
)
from .forms import (
    LoginForm,
    TagForm,
    MovieForm,
    PreviewForm,
    PwdForm,
)
from app.models import (
    Admin,
    Movietag,
    Movie,
    Preview,
    User,
    Comment,
    Movie_col,
    Oplog,
    Adminlog,
    Userlog,
)
from app import (
    app,
    db,
)
from functools import wraps
from werkzeug.utils import secure_filename
import os, uuid, datetime


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    # print("filename debug1",fileinfo[-1])
    filename = datetime.datetime.now().strftime("Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


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
            flash("密码错误！", "error")
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        adminlog = Adminlog(
            admin_id=admin.id,
            ip=request.remote_addr,
        )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(url_for("admin.index") or request.args.get("next"))
    return render_template("admin/login.html", form=form)


# 管理员登出
@admin.route("/logout")
@admin_login_required
def logout():
    session.pop("admin", None)
    return redirect(url_for('admin.login'))


# 修改密码
@admin.route("/pwd", methods=['GET', 'POST'])
@admin_login_required
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        newpwd = data['new_pwd']
        admin = Admin.query.filter_by(name=session['admin']).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(newpwd)
        db.session.add(admin)
        db.session.commit()
        flash("密码修改成功，请重新登录！", 'ok')
        return redirect(url_for('admin.logout'))
    return render_template("admin/pwd.html", form=form)


# 添加标签
@admin.route("/tag_add", methods=["GET", "POST"])
@admin_login_required
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Movietag.query.filter_by(name=data["name"]).count()
        if tag == 1:
            flash("名称已经存在！", "error")
            return redirect(url_for("admin.tag_add"))
        tag = Movietag(
            name=data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        admin = Admin.query.filter_by(name=session['admin']).first()
        oplog = Oplog(
            admin_id=admin.id,
            ip=request.remote_addr,
            reason="添加标签{name}成功！".format(name=data["name"])
        )
        db.session.add(oplog)
        db.session.commit()
        flash("添加标签成功", "ok")
        return redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 编辑标签
@admin.route("/tag_edit/<int:id>", methods=["GET", "POST"])
@admin_login_required
def tag_edit(id=None):
    form = TagForm()
    tag = Movietag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Movietag.query.filter_by(name=data["name"]).count()
        if tag_count == 1 and tag.name != data["name"]:
            flash("名称已经存在！", "error")
            return redirect(url_for("admin.tag_edit", id=id))
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功", "ok")
        return redirect(url_for("admin.tag_edit", id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 标签列表
@admin.route("/tag_list/<int:page>", methods=["GET"])
@admin_login_required
def tag_list(page):
    if page is None:
        page = 1
    # 分页信息
    page_data = Movietag.query.order_by(
        Movietag.addtime
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 标签删除
@admin.route("/tag_del/<int:id>", methods=["GET"])
@admin_login_required
def tag_del(id=None):
    tag = Movietag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签成功", "ok")
    return redirect(url_for("admin.tag_list", page=1))


# 添加电影
@admin.route("/movie_add", methods=["GET", "POST"])
@admin_login_required
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        movie = Movie.query.filter_by(title=data["title"]).count()
        if movie == 1:
            flash("名称已经存在！", "error")
            return redirect(url_for("admin.movie_add"))
        file_url = form.url.data.filename
        file_logo = form.logo.data.filename
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UP_DIR'] + url)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        movie = Movie(
            title=data["title"],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            play_num=0,
            comment_num=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length'],
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功！", "ok")
        return redirect(url_for("admin.movie_add"))
    return render_template("admin/movie_add.html", form=form)


# 编辑电影
@admin.route("/movie_edit/<int:id>", methods=["GET", "POST"])
@admin_login_required
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(id)
    if request.method == "GET":
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data["title"]).count()
        if movie_count == 1 and movie.title != data["title"]:
            flash("片名已经存在！", "error")
            return redirect(url_for("admin.movie_edit", id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')

        if form.url.data.filename != "":
            file_url = form.url.data.filename
            movie.url = change_filename(file_url)
            form.url.data.save(app.config['UP_DIR'] + movie.url)

        if form.logo.data.filename != "":
            file_logo = form.logo.data.filename
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + movie.logo)

        # 修改
        movie.title = data["title"]
        movie.star = data["star"]
        movie.tag_id = data["tag_id"]
        movie.info = data["info"]
        movie.area = data["area"]
        movie.length = data["length"]
        movie.release_time = data["release_time"]
        # 保存
        db.session.add(movie)
        db.session.commit()
        flash("修改电影成功", "ok")
        return redirect(url_for("admin.movie_edit", id=id))
    return render_template("admin/movie_edit.html", form=form, movie=movie)


# 电影列表
@admin.route("/movie_list/<int:page>", methods=["GET"])
@admin_login_required
def movie_list(page):
    if page is None:
        page = 1
    # 分页信息
    page_data = Movie.query.join(Movietag).filter(
        Movietag.id == Movie.tag_id
    ).order_by(
        Movie.addtime
    ).paginate(page=page, per_page=10)
    return render_template("admin/movie_list.html", page_data=page_data)


# 电影删除
@admin.route("/movie_del/<int:id>", methods=["GET"])
@admin_login_required
def movie_del(id=None):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    flash("删除电影成功", "ok")
    return redirect(url_for("admin.movie_list", page=1))


# 添加预告
@admin.route("/preview_add", methods=["GET", "POST"])
@admin_login_required
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        preview = Preview.query.filter_by(title=data['title']).count()
        if preview == 1:
            flash("名称已经存在！", "error")
            return redirect(url_for("admin.preview_add"))
        file_logo = form.logo.data.filename
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        logo = change_filename(file_logo)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        preview = Preview(
            title=data['title'],
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()
        flash("添加预告成功", "ok")
        return redirect(url_for("admin.preview_add"))
    return render_template("admin/preview_add.html", form=form)


# 预告列表
@admin.route("/preview_list/<int:page>", methods=["GET"])
@admin_login_required
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime
    ).paginate(page=page, per_page=10)
    return render_template("admin/preview_list.html", page_data=page_data)


# 预告删除
@admin.route("/preview_del/<int:id>", methods=["GET"])
@admin_login_required
def preview_del(id=None):
    preview = Preview.query.get_or_404(id)
    db.session.delete(preview)
    db.session.commit()
    flash("删除电影成功", "ok")
    return redirect(url_for("admin.preview_list", page=1))


# 编辑预告
@admin.route("/preview_edit/<int:id>", methods=["GET", "POST"])
@admin_login_required
def preview_edit(id=None):
    form = PreviewForm()
    form.logo.validators = []
    preview = Preview.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        preview_count = Preview.query.filter_by(title=data["title"]).count()
        if preview_count == 1 and preview.title != data["title"]:
            flash("预告已经存在！", "error")
            return redirect(url_for("admin.preview_edit", id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')

        if form.logo.data.filename != "":
            file_logo = form.logo.data.filename
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + preview.logo)

        # 修改
        preview.title = data["title"]
        # 保存
        db.session.add(preview)
        db.session.commit()
        flash("修改预告成功", "ok")
        return redirect(url_for("admin.preview_edit", id=id))
    return render_template("admin/preview_edit.html", form=form, preview=preview)


# 会员列表
@admin.route("/user_list/<int:page>", methods=["GET"])
@admin_login_required
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime
    ).paginate(page=page, per_page=10)
    return render_template("admin/user_list.html", page_data=page_data)


# 查看会员
@admin.route("/user_view/<int:id>", methods=["GET"])
@admin_login_required
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user)


# 删除会员
@admin.route("/user_del/<int:id>", methods=["GET"])
@admin_login_required
def user_del(id=None):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("删除会员成功", "ok")
    return redirect(url_for("admin.user_list", page=1))


# 评论列表
@admin.route("/comment_list/<int:page>", methods=['GET'])
@admin_login_required
def comment_list(page):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Movie_col.movie_id,
        User.id == Movie_col.user_id
    ).order_by(
        Comment.addtime
    ).paginate(page=page, per_page=10)
    return render_template("admin/comment_list.html", page_data=page_data)


# 删除评论
@admin.route("/comment_del/<int:id>", methods=["GET"])
@admin_login_required
def comment_del(id=None):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash("删除评论成功", "ok")
    return redirect(url_for("admin.comment_list", page=1))


# 电影收藏列表
@admin.route("/moviecol_list/<int:page>", methods=['GET'])
@admin_login_required
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = Movie_col.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Movie_col.movie_id,
        User.id == Movie_col.user_id
    ).order_by(
        Movie_col.addtime
    ).paginate(page=page, per_page=10)
    return render_template("admin/moviecol_list.html", page_data=page_data)


# 删除收藏
@admin.route("/moviecol_del/<int:id>", methods=["GET"])
@admin_login_required
def moviecol_del(id=None):
    moviecol = Movie_col.query.get_or_404(id)
    db.session.delete(moviecol)
    db.session.commit()
    flash("删除收藏成功", "ok")
    return redirect(url_for("admin.moviecol_list", page=1))


# 操作日志列表
@admin.route("/oplog_list/<int:page>", methods=['GET'])
@admin_login_required
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(
        Admin
    ).filter(
        Admin.id == Oplog.admin_id,
    ).order_by(
        Oplog.addtime
    ).paginate(page=page, per_page=10)
    return render_template("admin/oplog_list.html", page_data=page_data)


# 管理员登录日志列表
@admin.route("/adminloginlog_list/<int:page>", methods=['GET'])
@admin_login_required
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Adminlog.query.join(
        Admin
    ).filter(
        Admin.id == Adminlog.admin_id,
    ).order_by(
        Adminlog.addtime
    ).paginate(page=page, per_page=10)
    return render_template("admin/adminloginlog_list.html", page_data=page_data)


# 会员登录日志列表
@admin.route("/userloginlog_list/<int:page>", methods=['GET'])
@admin_login_required
def userloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.join(
        User
    ).filter(
        User.id == Userlog.user_id,
    ).order_by(
        Userlog.addtime
    ).paginate(page=page, per_page=10)
    return render_template("admin/userloginlog_list.html", page_data=page_data)


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
