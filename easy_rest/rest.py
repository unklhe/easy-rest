"""This is a makeup for urllib2 to access Rest API


It supports POST, GET, PUT, DELETE and PATCH, works for Python 2.7.6+.
"""
import logging
try:
    # For Python 3.0 and later
    from urllib import request as url_lib
    from urllib.error import HTTPError
except ImportError:
    # Fall back to Python 2's urllib2
    import urllib2 as url_lib
    from urllib2 import HTTPError
import ssl
import sys
import json

__logger = logging.getLogger("easy_rest")


# Support non-verification SSL requests
__ssl_context = None
try:
    __ssl_context = ssl.create_default_context()
    __ssl_context.check_hostname = False
    __ssl_context.verify_mode = ssl.CERT_NONE
except AttributeError:
    pass
if __ssl_context:
    def openurl(req):
        return url_lib.urlopen(req, context=__ssl_context)
else:
    def openurl(req):
        return url_lib.urlopen(req)


def __method__(url, data, **headers):
    method = sys._getframe(1).f_code.co_name.upper()
    __logger.debug("%s %s" % (method, url))
    if data:
        if type(data) not in [str, unicode]:
            data = json.dumps(data)
        __logger.debug(str(data))
    req = url_lib.Request(url, data, headers)
    req.get_method = lambda: method
    try:
        resp = openurl(req)
        return resp
    except HTTPError as e:
        return e

def post(url, data, **kwargs):
    return __method__(url, data, **kwargs)

def get(url, **kwargs):
    return __method__(url, None, **kwargs)

def put(url, data, **kwargs):
    return __method__(url, data, **kwargs)

def delete(url, **kwargs):
    return __method__(url, None, **kwargs)

def patch(url, data, **kwargs):
    return __method__(url, data, **kwargs)






