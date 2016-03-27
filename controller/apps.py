# -*- coding: utf-8 -*-
__author__ = 'ninad'


from flask import Blueprint, render_template, current_app, request, jsonify

apps = Blueprint('application', __name__, url_prefix='/apps')


@apps.route('/')
def listing():
    return render_template('apps/listing.html')
