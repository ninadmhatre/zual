__author__ = 'ninad'

import os
import simplejson as json
import hashlib
from urllib import parse


class Utility(object):
    @staticmethod
    def write_to_file(filename, content, as_json=False, safe=False):
        if safe:
            return Utility.safe_write_to_file(filename, content, as_json)

        with open(filename, 'w') as f:
            if as_json:
                f.write(json.dumps(content, indent=4))
            else:
                f.write(content)

    @staticmethod
    def read_from_file(filename, as_json=False, safe=False):
        if safe:
            return Utility.safe_read_from_file(filename, as_json)

        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                content = f.read()  # Read full file
                if as_json:
                    data = json.loads(content, encoding='utf-8')
                    return data, None
                return content, None

    @staticmethod
    def safe_read_from_file(filename, as_json=False):
        try:
            with open(filename, 'r+') as f:
                content = f.read()  # Read full file
                if as_json:
                    data = json.loads(content, encoding='utf-8')
                    return data, None
                return content, None
        except IOError as e:
            return False, e
        except ValueError as e:
            return False, e

    @staticmethod
    def safe_write_to_file(filename, content, as_json=False):
        try:
            with open(filename, 'w+') as f:
                if as_json:
                    f.write(json.dumps(content, indent=4))
                else:
                    f.write(content)
        except IOError as e:
            return False, e
        except ValueError as e:
            return False, e
        else:
            return True, None

    @staticmethod
    def get_ip(request):
        if 'HTTP_X_REAL_IP' in request.environ:
            return request.environ['HTTP_X_REAL_IP']
        elif 'HTTP_X_FORWARDED_FOR' in request.environ:
            ips = request.environ['HTTP_X_FORWARDED_FOR']
            return ips.split(',')[0]
        else:
            return request.remote_addr

    @staticmethod
    def get_md5_hash(string):
        if string and isinstance(string, str):
            return hashlib.md5(string.encode('utf-8')).hexdigest()

    @staticmethod
    def get_md5_hash_of_title(string):
        if string:
            _title = parse.quote(string)
            return hashlib.md5(_title.encode('utf-8')).hexdigest()
        return None

    @staticmethod
    def quote_string(string):
        if string:
            return parse.quote(string)

    @staticmethod
    def unquote_string(string):
        if string:
            return parse.unquote(string, encoding='utf-8')
