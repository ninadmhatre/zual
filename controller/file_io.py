# -*- coding: utf-8 -*-
__author__ = 'ninad'

import os
import shutil

from flask import Blueprint, render_template, abort, request, flash, send_from_directory
from flask.ext.login import login_required
from werkzeug import secure_filename

from application import app, stat
from libs.Utils import Utility

fileio = Blueprint('fileio', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}


@fileio.route('/img/<path:img_path>', methods=['GET'])
def get_img(img_path):
    ext = os.path.basename(img_path).split('.')[-1]
    if ext and ext in app.config['IMAGE_VALID_EXTS']:
        return send_from_directory(app.config['IMAGE_FOLDER'], img_path)
    else:
        abort(404)


@fileio.route('/doc/<path:doc_path>', methods=['GET'])
def get_doc(doc_path):
    ext = os.path.basename(doc_path).split('.')[-1]
    if ext and ext in app.config['DOCS_VALID_EXTS']:
        stat.update_download_count(doc_path, Utility.get_ip(request))
        return send_from_directory(app.config['DOCS_FOLDER'], doc_path, as_attachment=True)
    else:
        abort(404)


@fileio.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # import pdb
    # pdb.set_trace()
    if request.method == "POST":
        typ = request.form.get('type')
        file = request.files.get('file')
        result = False
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_as = os.path.join(app.config['UPLOAD_DIR'], filename)
            try:
                file.save(save_as)
            except Exception as e:
                return render_template('error_code/404.html', msg='Failed to save file...[Err:{0}]'.format(e))
            else:
                result = move_file(typ, save_as, filename, backup=True, linkit=True)

        if not result:
            flash('error:Failed To Upload file..., Try again...')
        else:
            flash('info:File uploaded Successfully!')

    return render_template('upload/upload.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def __move(src, dst, backup, linkit, link_name):
    if backup and os.path.isfile(dst):
        import datetime
        now = datetime.datetime.utcnow()
        now = now.strftime('%Y%m%d%H%M%S')
        shutil.move(dst, "{0}_{1}".format(dst, now))

    try:
        shutil.move(src, dst)
    except OSError:
        return False

    if linkit and link_name:
        # Change the link creation to be relative to current directory to avoid link failing across dev & prod setup
        # Like, if you create link and upload that will copy the link path the git, this will break prod
        # Hopefully, this will solve the issue
        _old_pwd = os.path.abspath('.')
        os.chdir(os.path.dirname(dst))
        result = True
        if os.path.islink(link_name):
            try:
                os.remove(link_name)
            except OSError:
                result = False
            else:
                os.symlink(os.path.basename(dst), link_name)
            finally:
                os.chdir(_old_pwd)
                return result


def move_file(typ, src, name, backup=True, linkit=True):
    result = False
    link_names = {'dp': 'dp.jpg', 'resume': 'Resume.docx'}
    if typ == 'dp':
        target = os.path.join(app.config['IMAGE_FOLDER'], name)
        result = __move(src, target, backup, linkit, link_names.get('dp'))
    elif typ == 'resume':
        target = os.path.join(app.config['DOCS_FOLDER'], name)
        result = __move(src, target, backup, linkit, link_names.get('resume'))
    elif typ == 'blog':
        target = os.path.join(app.config['IMAGE_FOLDER'], name)
        result = __move(src, target, backup=False, linkit=False, link_name=None)

    return result
