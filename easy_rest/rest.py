"""This is a makeup for urllib2 to access Rest API


It supports POST, GET, PUT, DELETE and PATCH, works for Python 2.7.6+.
"""
import logging
import urllib2
import ssl
import sys

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
        return urllib2.urlopen(req, context=__ssl_context)
else:
    def openurl(req):
        return urllib2.urlopen(req)


def __method__(url, data, **headers):
    method = sys._getframe(1).f_code.co_name.upper()
    __logger.debug("%s %s" % (method, url))
    if data:
        if type(data) is not str:
            data = str(data)
        __logger.debug(str(data))
    req = urllib2.Request(url, data, headers)
    req.get_method = lambda: method
    try:
        print req
        resp = openurl(req)
        return resp
    except urllib2.HTTPError, e:
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






