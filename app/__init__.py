# 项目app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import render_template
import pymysql


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost:3306/movie_db?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "secret key"

app.debug = True

db = SQLAlchemy(app)


from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')

# 404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
