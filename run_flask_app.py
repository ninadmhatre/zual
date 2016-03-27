__author__ = 'ninad'

from application import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True)
