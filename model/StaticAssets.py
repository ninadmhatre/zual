__author__ = 'ninad'

# Flask
from flask.ext.assets import Bundle, Environment
from application import app


bundles = {
    'third_party_js': Bundle(
        'js/jquery-2.1.3.min.js',
        'js/jquery-ui.min.js',
        'js/bootstrap.js',
        'js/toastr.min.js',
        'js/freelancer.js',
        'js/run_prettify.js',
        'js/site_personal.js',
        'js/prettify.js',
        'js/run_prettify.js',
        'js/classie.js',
        'js/socialShare.min.js',
        'js/cbpAnimatedHeader.js',
        filters='jsmin'
        ),

    'third_party_css': Bundle(
        'css/jquery-ui.min.css',
        'css/font-awesome.min.css',
        'css/bootstrap.min.css',
        'css/prettify.css',
        'css/site_personal.css',
        'css/arthref.min.css',
        'css/toastr.min.css',
        'css/freelancer.css',
        filters='cssmin'
    )
}

site_assets = Environment(app)
site_assets.register(bundles)


def get_assets():
    print('Here from lblrsm.assets....')
    return site_assets

