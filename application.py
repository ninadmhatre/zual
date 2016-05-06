# -*- coding: utf-8 -*-
__author__ = 'ninad'

# Core
import os
from datetime import timedelta

import custom_filter


# Flask
from flask import Flask, render_template, redirect, request, session, flash, send_from_directory, abort, url_for
from flask.ext.cache import Cache
from sqlalchemy import create_engine, MetaData
from flask.ext.login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask.ext.blogging import SQLAStorage, BloggingEngine
from flask.ext.seasurf import SeaSurf


# App
from model.StatsCollector import Stats
from libs.AppLogger import AppLogger, LoggerTypes
from libs.Mailer import Mailer
from libs.Informer import SqliteStorage, Informer

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

_static_folder = os.path.join(BASE_DIR, 'static')
instance_dir = os.path.join(BASE_DIR, 'instance')
blog_posts_dir = os.path.join(BASE_DIR, 'templates', 'blog')
upload_dir = os.path.join(BASE_DIR, 'uploads')

app = Flask(__name__, instance_path=instance_dir, static_path=_static_folder, static_url_path='/static')
# Trying on Windows? Comment out __above__ line and use __below__ line!
# app = Flask(__name__, instance_path=instance_dir, static_path='/static', static_url_path='/static')

app.config.from_object('instance.default')
app.config.from_object('instance.{0}'.format(os.environ.get('APP_ENVIRONMENT', 'dev')))
app.config['BASE_DIR'] = BASE_DIR
app.config['UPLOAD_DIR'] = upload_dir

custom_logger = AppLogger(app.config['LOGGER'])
app.logger.addHandler(custom_logger.get_log_handler(LoggerTypes.File))

if not app.config['DEBUG']:
    cache = Cache(config=app.config.get('CACHE')['redis'])
else:
    cache = Cache(config={'CACHE_TYPE': 'simple'})

mailer = Mailer(app)
cache.init_app(app)
csrf = SeaSurf(app)

engine = create_engine('sqlite:///blog.db')
meta = MetaData()

sql_storage = SQLAStorage(engine, metadata=meta)
blog_engine = BloggingEngine(app, sql_storage, cache=cache)
login_manager = LoginManager(app)
meta.create_all(bind=engine)

page_view_engine = create_engine('sqlite:///stats.db')
page_view_meta = MetaData()

page_view_storage = SqliteStorage(page_view_engine, metadata=page_view_meta)
page_view_meta.create_all(bind=page_view_engine)
page_view_stats = Informer(page_view_storage)

stat = Stats(app.config["STATS_FOLDER"])

app.logger.info('Starting Application')

# Login manager settings

login_manager.session_protection = "strong"

class User(UserMixin):
    """
    User Mixin; with get name being changed!
    """
    def __init__(self, user_id):
        self.id = user_id

    def get_name(self):
        # This is personal site, so default it's single/owner name!
        return "Test_User"


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = app.config['SESSION_TIMEOUT']

@login_manager.needs_refresh_handler
def refresh():
    return redirect(url_for('auth.login'))


@login_manager.user_loader
@blog_engine.user_loader
def load_user(user_id):
    """
    This is called for every request to get the user name
    :param user_id:
    :return:
    """
    return User(user_id)


# Initialize Other Modules
# Modules which requires instance of 'app' to be created first!
from model.StaticAssets import site_assets

site_assets.init_app(app)


@app.route('/')
def home():
    """
    Any guesses?
    :return:
    """
    return render_template('freelancer.html')


@app.errorhandler(404)
def page_not_found(e):
    """
    Flask does not support having error handler in different blueprint!
    :param e: error
    :return: error page with error code
    """
    return render_template('error_code/404.html'), 404


@app.errorhandler(401)
def page_not_found(e):
    """
    Flask does not support having error handler in different blueprint!
    :param e: error
    :return: error page with error code
    """
    return render_template('error_code/401.html'), 401


@app.errorhandler(500)
def internal_server_error(e):
    """
    Flask does not support having error handler in different blueprint!
    :param e: error
    :return: error page with error code
    """
    return render_template('error_code/500.html'), 500


@app.route('/test')
def test():
    d = {}
    for p in dir(request):
        d[p] = getattr(request, p)

    return render_template('dump/dict.html', data=d)

# Code Separated to Blueprints!

from controller.file_io import fileio
from controller.authentication import auth
from controller.admin import admin
from controller.apps import apps
from controller.api import api

app.register_blueprint(fileio)
app.register_blueprint(auth)
app.register_blueprint(apps)
app.register_blueprint(admin)
app.register_blueprint(api)


if __name__ == '__main__':
    app.run(port=app.config['PORT'])
