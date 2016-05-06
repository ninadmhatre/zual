# -*- coding: utf-8 -*-
__author__ = 'ninad'

import hashlib
import datetime
import pdb

from flask import Blueprint, render_template, abort, current_app, request, flash, redirect, url_for, session, g
from flask.ext.login import login_user, logout_user, login_required

from application import User, mailer, app
from itsdangerous import URLSafeTimedSerializer
from collections import namedtuple

auth = Blueprint('auth', __name__)


chaabi = 'your_password_123'  # <-- EDIT_THIS

MailInfo = namedtuple('MailInfo', 'Sender To Message Subject')

MAX_FAILED_ATTEMPTS = 2
DISABLE_LOGIN_FOR = 15 * 60
DISABLE_LOGIN = False
NOTIFIED = False

_failed_cnt = 0
_last_attempt = datetime.datetime.utcnow()

ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])
email_confirm_key = 'some other secret key'  # <-- EDIT_THIS


def authenticate(u, p):
    if u and p:
        if u in (current_app.config['ADMIN_MAIL'],):
            p_salt = p + current_app.config["SECRET_KEY"]
            e_salt = chaabi + current_app.config["SECRET_KEY"]

            d = hashlib.sha384()
            e = hashlib.sha384()

            d.update(p_salt.encode())
            e.update(e_salt.encode())
            return d.hexdigest() == e.hexdigest()
        else:
            return False
    else:
        return False


def notify_admin(msg):
    global NOTIFIED

    if NOTIFIED:
        return

    print('Sending Warning email...{0}'.format(msg))
    token = ts.dumps(current_app.config['ADMIN_MAIL'], salt=email_confirm_key)
    url = url_for('auth.enable', token=token, _external=True)

    data = '''<h3>Login Disabled!!</h3><br>
    <p>Please use below link in within next 72 hours to re-enable the login!</p><br>

    Enable Link: <a href="{0}">{0}</a>

    <p style="color: red; font-size: 80%">Note: In Case you fail to re-enable login, please bounce the site!
    Sorry but this is the best i could think at this moment!!!</p>
    '''.format(url)

    print('data -> {0}'.format(data))
    mail_details = MailInfo('alert@<< your_domain_com >>', current_app.config['ADMIN_MAIL'], 'Login Disabled!', data)
    mailer.send_simple_mail(mail_details)
    NOTIFIED = True


def disable_login():
    global DISABLE_LOGIN
    DISABLE_LOGIN = True


def guard(stage):
    """
    Last failed attempt should be at least done within 15 mins from now!
    :param stage:
    :return:
    """
    global _failed_cnt, _last_attempt

    if stage == 'GET':
        if _failed_cnt > MAX_FAILED_ATTEMPTS:
            notify_admin('Warning: Maximum failed attempts reached!')
            disable_login()
        else:
            since_last_attempt = datetime.datetime.utcnow() - _last_attempt
            if since_last_attempt.total_seconds() > DISABLE_LOGIN_FOR:
                _last_attempt = datetime.datetime.utcnow()
                _failed_cnt += 0
    elif stage == 'POST':
        _failed_cnt += 1
        _last_attempt = datetime.datetime.utcnow()
        print('Failed login attempt! {0}/{1} attempts...'.format(_failed_cnt, MAX_FAILED_ATTEMPTS))


@auth.route("/login/", methods=['GET', 'POST'])
def login():
    session.permanent = True
    #pdb.set_trace()
    if DISABLE_LOGIN:
        flash('error:Login is disable because of many failed login attempts!')
        return render_template('login/login.html', disable=True)

    if request.method == 'POST':
        user = request.form['user']
        pawd = request.form['chaabi']

        if not authenticate(user, pawd):
            guard('POST')
            flash("error:Invalid Username or Password!")
            #return render_template('login/login.html')
        else:
            flash("info:Login Successful!")
            user = User("test_user")
            login_user(user)
            return redirect("/blog")
    guard('GET')
    return render_template('login/login.html')


@auth.route("/enable/<token>", methods=['GET', 'POST'])
def enable(token):
    email = ''
    try:
        email = ts.loads(token, salt=email_confirm_key, max_age=84600 * 3)
    except:
        flash('error:Invalid Enable Link!!')
        abort(404)

    if email == current_app.config['ADMIN_MAIL']:
        global DISABLE_LOGIN, NOTIFIED
        DISABLE_LOGIN = False
        NOTIFIED = False
    else:
        flash('error:Invalid Enable Link!!!')
        abort(404)

    flash('info:Account enabled successfully!')
    return redirect(url_for('auth.login'))


@auth.route("/logout/")
def logout():
    logout_user()
    flash('info:User Logged Out Successfully!')
    return redirect("/")
