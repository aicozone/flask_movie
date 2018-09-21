# 表单处理文件
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.validators import (
    DataRequired,
    ValidationError,
)
from app.models import Admin


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            "required": "required",
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
            "required": "required",
        }
    )
    submit = SubmitField(
        "登录",
        render_kw = {
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
    name = StringField(
        label="标签名称",
        validators=[
            DataRequired("请输入标签名称！")
        ],
        description="标签",
        render_kw={
            "class":"form-control",
            "id":"input_name",
            "placeholder":"请输入标签名称！"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary",
        }
    )
