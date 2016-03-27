# -*- coding: utf-8 -*-
__author__ = 'ninad'

# Core
import os

import custom_filter


# Flask
from flask import Flask, render_template, redirect, request, flash, send_from_directory, abort, url_for
from flask.ext.cache import Cache
from sqlalchemy import create_engine, MetaData
from flask.ext.login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask.ext.blogging import SQLAStorage, BloggingEngine

# App
from model.StatsCollector import Stats
from libs.AppLogger import AppLogger, LoggerTypes
from libs.Mailer import Mailer

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
app.config['UPLOAD_DIR'] = upload_dir

custom_logger = AppLogger(app.config['LOGGER'])
app.logger.addHandler(custom_logger.get_log_handler(LoggerTypes.File))

if not app.config['DEBUG']:
    cache = Cache(config=app.config.get('CACHE')['redis'])
else:
    cache = Cache(config={'CACHE_TYPE': 'simple'})

mailer = Mailer(app)

cache.init_app(app)

engine = create_engine('sqlite:///blog.db')
meta = MetaData()

sql_storage = SQLAStorage(engine, metadata=meta)
blog_engine = BloggingEngine(app, sql_storage, cache=cache)
login_manager = LoginManager(app)
meta.create_all(bind=engine)

stat = Stats(app.config["STATS_FOLDER"])

app.logger.info('Starting Application')
# TODO: Add Key to stop XSS


class User(UserMixin):
    """
    User Mixin; with get name being changed!
    """
    def __init__(self, user_id):
        self.id = user_id

    def get_name(self):
        # This is personal site, so default it's single/owner name!
        return "Test_User"


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
@cache.cached(timeout=600)
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


# Code Separated to Blueprints!

from controller.file_io import fileio
from controller.authentication import auth
from controller.dashboard import dash
from controller.apps import apps

app.register_blueprint(fileio)
app.register_blueprint(auth)
app.register_blueprint(apps)
app.register_blueprint(dash)


if __name__ == '__main__':
    app.run(port=app.config['PORT'])
