# -*- coding: utf-8 -*-
__author__ = 'ninad'

import pdb
import os

from flask import Blueprint, render_template, abort, current_app, request, flash, redirect, url_for
from flask.ext.login import login_required

from application import app, stat, blog_engine, BASE_DIR

dash = Blueprint('dash', __name__)

from addonpy.addonpy import AddonHelper, AddonLoader

# Dashboard will/should list
# 1. Resume download count
# 2. List of all posts and their read count!
# 3. It should be protected!
# 4. Status of gunicorn & redis process
# 5. Redis cache status (memory and process)
# 6. Server processes

module_list = None

def load():
    loader = AddonLoader(verbose=True, logger=app.logger, recursive=False, lazy_load=False)
    loader.set_addon_dirs([os.path.join(BASE_DIR, app.config['DASHBOARD_MODS'])])
    loader.set_addon_methods(['execute', 'template', 'get_result'])
    loader.load_addons()
    return loader, loader.get_loaded_addons(list_all=True)


def run(loader, mod):
    if mod != 'SiteStatsAddon':
        mod_inst = loader.get_instance(mod)
        mod_inst.print_addon_info()
        mod_inst.execute(current_app.config)
        return mod_inst.get_result(as_html=True)

@dash.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    #pdb.set_trace()
    global module_list
    loader, module_list = load()
    result = {}

    for module in module_list:
        result[module] = run(loader, module)

    return render_template('dashboard/dashboard.html', result=result)


@dash.route('/reload', methods=['GET'])
@login_required
def reload():
    global module_list
    module_list = load()
