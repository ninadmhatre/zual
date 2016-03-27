__author__ = 'ninad'

import logging
from datetime import timedelta
import os

DEBUG = True
LOG_QUERIES = False
SECRET_KEY = '<< Your Secret Key >>' 
PORT = 22000
ADMIN_MAIL = '<< your email address! one you check >>'
LOGGER = {
    'FILE': dict(FILE='logs/log.log',
                 LEVEL=logging.DEBUG,
                 NAME='web_logger',
                 HANDLER='File',
                 FORMAT='%(asctime)s %(levelname)s %(filename)s %(module)s [at %(lineno)d line] %(message)s',
                 EXTRAS=dict(when='D', interval=1, backupCount=7))
}

ASSETS_DEBUG = False

BLOGGING_URL_PREFIX = '/blog'
BLOGGING_DISQUS_SITENAME = 'Echo'

IMAGE_VALID_EXTS = ['jpg', 'jpeg', 'png']
DOCS_VALID_EXTS = ['doc', 'docx', 'xlsx', 'xls', 'pdf']

permanent_session_lifetime = timedelta(minutes=240)

CACHE = dict(redis=dict(
    CACHE_KEY_PREFIX='site',
    CACHE_DEFAULT_TIMEOUT=60,
    CACHE_TYPE='redis',
    CACHE_REDIS_HOST='localhost',
    CACHE_REDIS_PORT=9779
    )
)

# URL's

FACEBOOK = 'https://www.facebook.com/<< Your FB profile name >>'
GOOGLE_PLUS = 'https://plus.google.com/<< Your G+ Profile >>'
GIT_HUB = 'https://github.com/<< Your GitHub >>'
LINKED_IN = '<< linked in profile >>'
PERSONAL_EMAIL = '<< Personal Mail ID >>'

# Upload Folder
IMAGE_FOLDER = os.path.abspath('blog/img')
DOCS_FOLDER = os.path.abspath('blog/docs')
STATS_FOLDER = os.path.abspath('stats')

# Dashboard
DASHBOARD_MODS = 'dashboard_mods'

# Mail

__RELEASE__ = 'm4'
__VERSION__ = '2.3.27-0'  # Year.Month.Day-Patch Note: 2015 is 1
