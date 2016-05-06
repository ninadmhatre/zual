# -*- coding: utf-8 -*-
__author__ = 'ninad'

import pdb
import os
from collections import namedtuple
import json

from flask import Blueprint, render_template, abort, current_app, request, flash, redirect, url_for
from flask.ext.login import login_required

from application import app, stat, blog_engine, BASE_DIR, mailer, custom_logger
from libs.Utils import Utility

admin = Blueprint('admin', __name__)

from addonpy.addonpy import AddonHelper, AddonLoader
from cerberus import Validator, ValidationError, SchemaError

MailInfo = namedtuple('MailInfo', 'Sender To Message Subject')

# Dashboard will/should list
# 1. Resume download count
# 2. List of all posts and their read count!
# 3. It should be protected!
# 4. Status of gunicorn & redis process
# 5. Redis cache status (memory and process)
# 6. Server processes

log = custom_logger.get_stand_alone_logger()


def load():
    ldr = AddonLoader(verbose=True, logger=app.logger, recursive=False, lazy_load=False)
    ldr.set_addon_dirs([os.path.join(BASE_DIR, app.config['DASHBOARD_MODS'])])
    ldr.set_addon_methods(['execute', 'template', 'get_data', 'name'])
    ldr.load_addons()
    return ldr, ldr.get_loaded_addons(list_all=True)


def run(ldr, mod, req):
    mod_inst = ldr.get_instance(mod)
    mod_inst.print_addon_info()
    mod_inst.execute(current_app.config, req)
    return mod_inst.get_result(as_html=True)


loader, module_list = load()
alerts_file = os.path.join(BASE_DIR, 'files', 'alerts.txt')


@admin.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    global module_list, loader
    result = {}

    for module in module_list:
        result[module] = run(loader, module, request)

    return render_template('admin/dashboard.html', result=result)


@admin.route('/reload', methods=['GET'])
@login_required
def reload():
    global module_list
    module_list = load()


@admin.route('/mail_test', methods=['GET', 'POST'])
@login_required
def mail_test():
    if request.method == 'POST':
        from_addr = request.form.get('from_addr')
        to_addr = request.form.get('to_addr')
        subject = request.form.get('subject')
        content = request.form.get('body')

        mail_details = MailInfo(from_addr, to_addr, content, subject)
        current_app.logger.info('Sending Test Mail, details {0}'.format(mail_details))
        mailer.send_simple_mail(mail_details)
        flash('info:Mail Sent Successfully!')

    return render_template('admin/mail_test.html')


def parse_alert_data(data):
    current = {}
    for d in data.splitlines():
        header, text = d.split('=', 2)
        current[header] = text.strip('\n')

    return current


def update_alert_message(alert_file):
    data, err = Utility.safe_read_from_file(alert_file, as_json=False)
    if not err:
        # Ignore error to read file
        current = parse_alert_data(data)

        if current:
            app.jinja_env.globals['alert'] = current
            #flash('info:New Alert Message Setup Successfully!!')
            log.debug('Setup new alert message!')
    else:
        log.error('Failed to setup alert in jinja evn variable, Error: %s' % err)


update_alert_message(alerts_file)


@admin.route('/alert', methods=['GET', 'POST'])
def alert():
    if request.method == 'POST':
        _type = request.form.get('type')
        data = request.form.get('data')
        disabled = request.form.get('disable', False)

        disabled = True if disabled == 'on' else False

        text = 'type={0}\ntext={1}\ndisabled={2}\n'.format(_type, data, disabled)
        result, err = Utility.safe_write_to_file(alerts_file, text, as_json=False)

        if err:
            current_app.logger.error('Failed to create new alert! Error: %s' % err)
            flash('error:Failed to setup alert, please check the log and try again...')
            return redirect(url_for('admin.dashboard'))

        update_alert_message(alerts_file)

    current_alert = {}

    if os.path.isfile(alerts_file):
        data, err = Utility.safe_read_from_file(alerts_file, as_json=False)
        if err:
            current_app.logger.error('Failed to read alert file! Error: %s' % err)
            flash('error:Failed to read alert file, please check the log and try again!!')
            return redirect(url_for('admin.dashboard'))
        current_alert = parse_alert_data(data)

    return render_template('admin/alert.html', data=current_alert)


@admin.route('/notice_manage', methods=['POST'])
@login_required
def notice_manage():
    alerts_file = os.path.join(BASE_DIR, 'files', 'alerts.json')
    pdb.set_trace()

    action = request.form['notice_action']
    toggle_from = request.form['alert_stat']

    data, err = Utility.safe_read_from_file(alerts_file, as_json=True)
    if not err:
        if action == 'toggle':
            data['enabled'] = not data['enabled']
            ok, err = Utility.safe_write_to_file(alerts_file, data, as_json=True)
        elif action == 'replace':
            notice = request.form['setfor']
            parser = Notice(notice)

            try:
                key_count, ok = parser.parse()
                if ok:
                    # pdb.set_trace()
                    errors = parser.validate()
                    if errors:
                        return render_template('admin/site_message.html', error=errors, data=notice)

                    data = parser.result
            except Exception as e:
                return render_template('admin/site_message.html', error=e, data=notice)

            if ok:
                flash('info:Alert Disabled Successfully!')
                return redirect(url_for('admin.manage_notice'))
            else:
                flash('error:Falied To Disable Alert! Please Try Again...')
            return redirect(url_for('admin.manage_notice'))


@admin.route('/notice', methods=['GET', 'POST'])
@login_required
def manage_notice():
    data = {}
    alerts_file = os.path.join(BASE_DIR, 'files', 'alerts.json')

    if request.method == 'POST':
        notice = request.form['setfor']
        parser = Notice(notice)

        try:
            key_count, ok = parser.parse()
            if ok:
                # pdb.set_trace()
                errors = parser.validate()
                if errors:
                    return render_template('admin/site_message.html', error=errors, data=notice)
                data = parser.result
        except Exception as e:
            return render_template('admin/site_message.html', error=e, data=notice)

        ok, err = Utility.safe_write_to_file(alerts_file, data, as_json=True)
        if not ok:
            return render_template('admin/site_message.html', error=err)
        else:
            return render_template('admin/site_message.html', data=data)

    data, err = Utility.safe_read_from_file(alerts_file, as_json=True)
    if not err:
        return render_template('admin/site_message.html', data=data)


class Notice(object):
    def __init__(self, notice_str):
        self.data = notice_str
        self.schema = {'text': {'type': 'string', 'minlength': 1, 'required': True},
                       'type': {'type': 'string', 'allowed': ['info', 'warn', 'error'], 'minlength': 1, 'required': True},
                       'enabled': {'type': 'boolean', 'required': True},
                       'can_remove': {'type': 'boolean', 'required': True},
                       'set_for': {'type': 'list', 'required': True},
                       'unset_for': {'type': 'list', 'required': True},
                       }
        self.result = {}

    def parse(self):
        _n = self.data.replace('\r\n', '').strip(' ')
        print("[%s]" % _n)
        # '{text: "<h1>This is Heading</h1>",type: "info",enabled: "true",can_remove: "true",set_for: "",unset_for: "",}'
        _n = _n[1:-1]
        parts = _n.split(',')
        for entry in parts:
            if entry == '' or ':' not in entry:
                continue
            k, v = [i.strip(' ') for i in entry.split(':', 2)]
            self.result[k] = self._convert_to_py_types(v, k)

        return len(self.result), len(self.result) == len(self.schema)

    def validate(self):
        # pdb.set_trace()
        v = Validator(self.schema)
        status = v.validate(self.result)
        if not status:
            return v.errors
        return None

    def _convert_to_py_types(self, value, key_name):
        value = value.replace('"', '')
        if key_name in ('enabled', 'can_remove'):
            return value.lower() in ('yes', 'true')
        elif key_name in ('set_for', 'unset_for'):
            #value = value.replace(' ', '')
            if value == '':
                return []
            else:
                return value.split(',')

        else:
            return value
    def _text_to_type(self, txt_type):
        if txt_type.startswith('str'):
            return str
        elif txt_type.startswith('bool'):
            return bool
        elif txt_type.startswith('list'):
            return list
