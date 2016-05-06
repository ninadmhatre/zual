__author__ = 'ninad'

import logging
from datetime import timedelta
import os

DEBUG = True
LOG_QUERIES = False
SECRET_KEY = 'Secret_key' # <-- EDIT_THIS
PORT = 5000
ADMIN_MAIL = 'test.mail@yourdomain.com' # <-- EDIT_THIS
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
SESSION_TIMEOUT = timedelta(minutes=240)

CACHE = dict(redis=dict(
    CACHE_KEY_PREFIX='site',
    CACHE_DEFAULT_TIMEOUT=60,
    CACHE_TYPE='redis',
    CACHE_REDIS_HOST='localhost',
    CACHE_REDIS_PORT=9779
    )
)

# URL's

FACEBOOK = 'https://www.facebook.com/<< Your FB profile name >>'  # <-- EDIT_THIS
GOOGLE_PLUS = 'https://plus.google.com/<< Your G+ Profile >>'     # <-- EDIT_THIS
GIT_HUB = 'https://github.com/<< Your GitHub >>'                  # <-- EDIT_THIS
LINKED_IN = '<< linked in profile >>'                             # <-- EDIT_THIS
PERSONAL_EMAIL = ADMIN_MAIL

# Upload Folder
IMAGE_FOLDER = os.path.abspath('blog/img')
DOCS_FOLDER = os.path.abspath('blog/docs')
STATS_FOLDER = os.path.abspath('stats')

# Dashboard
DASHBOARD_MODS = 'dashboard_mods'

# Mail
MAIL_SERVER = ''  # <-- EDIT_THIS (Put mail server ), I am using zoho
MAIL_PORT = 465   # <-- EDIT_THIS
#MAIL_USE_TLS = True
MAIL_USE_SSL = True  # <-- EDIT_THIS
MAIL_USERNAME = 'alert@yourdomain.com'  # <-- EDIT_THIS
MAIL_PASSWORD = 'blah..blah'  # <-- EDIT_THIS
MAIL_DEFAULT_SENDER = 'alert@yourdomain.com'  # <-- EDIT_THIS

# Enable Page Counter
ENABLE_PAGE_COUNTER = True

__RELEASE__ = 'm4'
__VERSION__ = '2.5.05-0'  # Year.Month.Day-Patch Note: 2015 is 1
