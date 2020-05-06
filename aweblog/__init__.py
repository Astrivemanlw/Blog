from flask import Flask
from aweblog.app.post import post_app
from aweblog.app.auth import auth_app
from aweblog.app.manage import manage_app
from aweblog.extensions import moment, db, bootstrap, login_manager, csrf, ckeditor
# from flask_assets import Environment, Bundle
import os
import click
from faker import Faker
from aweblog.models import *


def create_app(config_name):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('aweblog', template_folder='../templates', static_folder='../static')
    app.config.from_pyfile('settings.py')
    app.config['FLASK_CONFIG'] = config_name
    register_extensions(app)
    # register_assets(app)
    register_blueprint(app)
    register_command(app)
    return app


# def register_assets(app):
#     assets = Environment(app)
#     css = Bundle('css/bootstrap.min.css',
#                  'css/font-awesome.min.css',
#                  'css/we.css',
#                  filters="cssmin", output="gen/packed.css")
#     js = Bundle('js/bootstrap.min.js',
#                 'js/jquery.min.js',
#                 'js/moment-with-locales.min.js',
#                 'js/popper.min.js',
#                 'js/script.js',
#                 'js/we.js',
#                 filters="jsmin", output="gen/packed.js")
#     assets.register('all_css', css)
# 
#     assets.register('all_js', js)


def register_extensions(app):
    moment.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    # cache.init_app(app)


def register_blueprint(app):
    # 注册模块
    app.register_blueprint(post_app)
    app.register_blueprint(auth_app, url_prefix='/auth')
    app.register_blueprint(manage_app, url_prefix='/manage')


def register_command(app):
    fake = Faker('zh_CN')

    @app.cli.command()
    def crt_db():
        """create aweblog db all table"""
        db.create_all()
        click.echo('create db successful')

    @app.cli.command()
    def drop_db():
        """drop aweblog db all table """

        db.drop_all()
        click.echo('create db successful')

    @app.cli.command()
    @click.option('--cn', default=20, help='number of fake data,default:20')
    def gen_fake_data(cn):
        """Generate fake data to test"""
        db.drop_all()
        db.create_all()
        for i in range(cn):
            post = Post(
                title=fake.word(),
                content=fake.text(),
                timestamp=fake.date_time_this_year(),
                catalog=fake.word(),
                love_count=fake.random_int(min=10, max=1000),
                read_count=fake.random_int(min=10, max=1000)

            )
            comment = Comment(
                author=fake.name(),
                content=fake.sentence(),
                email=fake.email(),
                site=fake.url(),
                is_admin=fake.boolean(),
                qualified=fake.boolean(),
                timestamp=fake.date_time_this_year(),
                post_id=fake.random_int(min=1, max=10),
                love_count=fake.random_int(min=10, max=1000)

            )

            db.session.add(post)
            db.session.add(comment)

        admin = Admin(username='admin')
        admin.password = 'admin123'

        db.session.add(admin)

        db.session.commit()
        click.echo('create fake data successfully')
