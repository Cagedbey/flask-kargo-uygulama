from logging import fatal
from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretpaswword123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


from blog.routes import admin

app.register_blueprint(admin)


from blog import routes