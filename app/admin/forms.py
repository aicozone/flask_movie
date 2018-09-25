# 表单处理文件
from flask import session
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    FileField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    ValidationError,
)
from app.models import (
    Admin,
    Movietag,
)

tags = Movietag.query.all()


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            "DataRequired": "DataRequired",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            "DataRequired": "DataRequired",
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        """验证账户"""
        account = field.data  # 这里的 field.data 相当于 form.account
        admin_num = Admin.query.filter_by(name=account).count()
        if admin_num == 0:
            raise ValidationError("账号不存在！")


class TagForm(FlaskForm):
    """标签管理表单"""
    name = StringField(
        label="标签名称",
        validators=[
            DataRequired("请输入标签名称！")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary",
        }
    )


class MovieForm(FlaskForm):
    """电影管理表单"""
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名！")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入片名！",
        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件",
        render_kw={
            "id": "input_url",
        }
    )
    info = TextAreaField(
        label="介绍",
        validators=[
            DataRequired("请输入介绍！")
        ],
        description="介绍",
        render_kw={
            "class": "form-control",
            "rows": "10",
            "id": "input_info",
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面",
        render_kw={
            "id": "input_logo",
        }
    )
    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "id": "input_star",
            "class": "form-control",
        }
    )
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description="标签",
        render_kw={
            "id": "input_tag_id",
            "class": "form-control",
        }
    )
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "id": "input_area",
            "placeholder": "请输入地区！",
        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("请输入片长！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            "id": "input_length",
            "placeholder": "请输入片长！",
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请输入上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "id": "input_release_time",
            "placeholder": "请输入上映时间！",
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary",
        }
    )


class PreviewForm(FlaskForm):
    """预告管理表单"""
    title = StringField(
        label='预告标题',
        validators=[
            DataRequired('请输入预告标题')
        ],
        description='预告标题',
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入预告标题！",
        }
    )
    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("请上传预告封面！")
        ],
        description="预告封面",
        render_kw={
            "id": "input_logo",
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class PwdForm(FlaskForm):
    """密码管理表单"""
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "id": "input_pwd",
            "placeholder": "请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "id": "input_newpwd",
            "placeholder": "请输入新密码！",
        }
    )
    submit = SubmitField(
        '修改',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    def validate_old_pwd(self, field):
        """验证旧密码"""
        old_pwd = field.data  # 这里的 field.data 相当于 form.account
        admin = Admin.query.filter_by(name=session['admin']).first()
        if not admin.check_pwd(old_pwd):
            raise ValidationError("旧密码错误！")
