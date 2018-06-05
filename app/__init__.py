from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import configs
from flask_admin import Admin
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
app_admin = Admin(name='Mock Server',template_mode='bootstrap3',url='/sdmockserver3')
bootstrap = Bootstrap()

def create_app(config_name):
    """Use factory to product app"""
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)
    db.init_app(app)

    app_admin.init_app(app)
    bootstrap.init_app(app)
    # set flask admin swatch
    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    # for admin-flask
    init_custom_view()

    print('^_^ APP is created ^_^')
    return app


def init_custom_view():
    from app import app_admin
    from app.main.views import CustomModelView
    from app.models import MockJson

    app_admin.add_view(CustomModelView(MockJson,db.session,category='新增'))