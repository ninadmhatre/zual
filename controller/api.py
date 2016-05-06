# -*- coding: utf-8 -*-
__author__ = 'ninad'


from flask import Blueprint, current_app, request, jsonify
from application import page_view_stats
import simplejson as json
from libs.Utils import Utility
import time

api = Blueprint('api', __name__, url_prefix='/api')

dumb_cache = {}


@api.route('/views', methods=['GET', 'POST'])
def view_counter():
    page_id = None
    if request.method == 'POST':
        data = json.loads(request.data)
        if 'page_title' not in data:
            return jsonify(view='Invalid Parameters Passed!!')

        title = data['page_title']
        page_id = Utility.get_md5_hash_of_title(title)
        current_app.logger.debug('Page Title : {0} & Page Id: {1}'.format(title, page_id))
        remote_ip = Utility.get_ip(request)
        update_page_count(page_id, title, remote_ip)

    result = page_view_stats.get_count(page_id)
    return jsonify(views=result['count'])


def update_page_count(page_id, title, remote_ip):
    joined = '{0}:{1}'.format(page_id, remote_ip)

    if joined in dumb_cache:
        last_time = dumb_cache[joined]
        now = time.time()
        if now - last_time > 180:
            if page_view_stats.update(page_id, is_page_id=True):
                dumb_cache[joined] = now
    else:
        if page_view_stats.insert(page_id, Utility.quote_string(title)):
            dumb_cache[joined] = time.time()
        else:
            current_app.logger.error('Failed to insert page_id [{0}] in page_view_counter'.format(page_id))
