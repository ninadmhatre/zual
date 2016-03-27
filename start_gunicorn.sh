/usr/bin/python3 /usr/local/bin/gunicorn --workers 3 --bind unix:/home/papps/ninadmhatre-com/pweb.sock --access-logfile tmp/access.log --error-logfile tmp/error.log wsgi:app
