# 数据模型文件, 包含用户, 用户日志, 标签, 电影, 上映预告, 评论, 收藏, 权限, 角色, 管理员登录日志, 管理员操作日志
from datetime import datetime
from app import db

# 用户
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志符
    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关联
    comments = db.relationship('Comment', backref='user')  # 评论外键关联
    movie_cols = db.relationship('Movie_col', backref='user')  # 评论外键关联

    def __repr__(self):
        return '<User %r>' % self.name


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 所属会员编号
    ip = db.Column(db.String(100))  # 最近登录ip地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 最近登录时间

    def __repr__(self):
        return '<Userlog %r>' % self.id


# 标签
class Movietag(db.Model):
    __tablename__ = "movietag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    # relationship是一对多的关系, 表明指向 Movie 类并 表明多部电影
    movies = db.relationship('Movie', backref='movietag')  # 电影外键关联

    def __repr__(self):
        return '<Movietag %r>' % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True) # 标题
    url = db.Column(db.String(255), unique=True)    # 存储地址
    info = db.Column(db.Text)   # 电影信息
    logo = db.Column(db.String(255), unique=True)   # 电影图标
    star = db.Column(db.SmallInteger)       # 电影评分
    play_num = db.Column(db.BigInteger)     # 播放量
    comment_num = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey("movietag.id"))    # 标签
    area = db.Column(db.String(255))    # 地区
    release_time = db.Column(db.Date)   # 上映时间
    length = db.Column(db.String(100))  # 片长
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 电影添加时间
    comments = db.relationship('Comment', backref='movie')  # 电影外键关联
    movie_cols = db.relationship('Movie_col', backref='movie')  # 电影外键关联

    def __repr__(self):
        return '<Movie %r>' % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Preview %r>' % self.title


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 评论时间

    def __repr__(self):
        return '<Comment %r>' % self.id


# 电影收藏
class Movie_col(db.Model):
    __tablename__ = "movie_col"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 评论时间

    def __repr__(self):
        return '<Movie_col %r>' % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 权限名称
    url = db.Column(db.String(255), unique=True)  # 所属电影
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Auth %r>' % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 权限名称
    auths = db.Column(db.String(600))  # 拥有权限
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship('Admin', backref='role')

    def __repr__(self):
        return '<Auth %r>' % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员, 0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = db.relationship('Adminlog', backref='admin')  # 管理员登录外键关联
    oplogs = db.relationship('Oplog', backref='admin')  # 管理员操作外键关联

    def __repr__(self):
        return '<Admin %r>' % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))  # 所属管理员编号
    ip = db.Column(db.String(100))  # 最近登录ip地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 最近登录时间

    def __repr__(self):
        return '<Adminlog %r>' % self.id


# 管理员操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))  # 所属管理员编号
    ip = db.Column(db.String(100))  # 最近登录ip地址
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 最近登录时间

    def __repr__(self):
        return '<Oplog %r>' % self.id

# if __name__ == "__main__":
#     # 创建表
#     # db.create_all()
#     # 删除表
#     # db.drop_all()
#     # role = Role(
#     #     name="超级管理员",
#     #     auths="",
#     # )
#     # db.session.add(role)
#     # db.session.commit()
#     # 插入管理员字段
#     from werkzeug.security import generate_password_hash
#     admin = Admin(
#         name="movie_test1",
#         pwd=generate_password_hash("123"),
#         is_super=0,
#         role_id=1,
#     )
#     db.session.add(admin)
#     db.session.commit()