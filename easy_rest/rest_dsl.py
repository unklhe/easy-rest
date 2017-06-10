import rest
import base64
import re
import json
import sys



class Response:

    def __init__(self, resp):
        """
        :type resp: object
        """
        self._response = resp
        self._url = resp.url
        self._raw_data = resp.read()
        self._status_code = resp.getcode()
        self._headers = resp.info()
        self._content_type = self._headers["Content-Type"] if "Content-Type" in self._headers else ""
        if re.match("^application/.*json$", self._content_type):
            self._content_type = "json"
        elif re.match("^application/.*xml$", self._content_type):
            self._content_type = "xml"
        elif re.match("^text/html.*$", self._content_type):
            if self._raw_data.strip() == "":
                self._content_type = "json"
                self._raw_data = "{}"
            else:
                try:
                    json.loads(self._raw_data)
                    self._content_type = "json"
                except ValueError:
                    pass
    @property
    def status_code(self):
        return self._status_code

    @property
    def content_type(self):
        return self._content_type

    @property
    def http_headers(self):
        return self._headers

    @property
    def body(self):
        return self._raw_data

    @property
    def data(self):
        if "json" in self._content_type:
            return json.loads(self._raw_data)
        return self._raw_data

    def __str__(self):
        msg = "[Request URL]\n"
        msg += self._url
        msg += "\n"
        msg += "[Response.Code]\n"
        msg += str(self._status_code)
        msg += "\n"
        msg += "[Response.Header]\n"
        align_width = 1
        for key in self._headers:
            if align_width < len(key):
                align_width = len(key)
        for key in self._headers:
            msg += "  %s: %s\n" % (key.ljust(align_width), self._headers[key])
        msg += "[Response.body]\n"
        msg += self._raw_data
        return msg

class ResponseError(Response, rest.HTTPError):

    def __init__(self, httperror):
        rest.HTTPError.__init__(self, 
                                httperror.url, 
                                httperror.code,
                                httperror.msg,
                                httperror.hdrs,
                                httperror.fp)
        Response.__init__(self, httperror)


class Connection:
    def __init__(self, host, service_path=None, **kwargs):
        self._headers = {}
        if "auth_type" in kwargs:
            auth_type = kwargs["auth_type"]
            if auth_type.lower() == "basic":
                username = kwargs["auth_user"]
                password = kwargs["auth_password"]
                cert = base64.b64encode(username + ":" + password)
                self._headers["Authorization"] = "Basic " + cert
                del kwargs["auth_user"]
                del kwargs["auth_password"]
            elif auth_type.lower() == "bearer":
                self._headers["Authorization"] = "bearer " + wargs["token"]
                del kwargs["token"]
            del kwargs["auth_type"]
        self._headers.update(kwargs)
        match_result = re.match("^(https://|http://|)(?P<host>.+)$", host)
        self._host = match_result.group("host")
        if self._host.endswith("/"):
            self._host = self._host[0: -1]
        if service_path and len(service_path) > 0:
            if service_path.startswith("/"):
                service_path = service_path[1:]
            if service_path.endswith("/"):
                service_path = service_path[0:-1]
            if len(service_path) > 0:
              self._host += "/" + service_path
        is_ssl = (match_result.group(1) == "https://")
        if "port" in kwargs:
            self._host += ":" + kwargs["port"]
        if is_ssl:
            self._host = "https://" + self._host
        else:
            self._host = "http://" + self._host

    def __method__(self, resource, *args, **kwargs):
        method = sys._getframe(1).f_code.co_name
        headers = self._headers.copy()
        headers.update(kwargs)
        if args and type(args[0]) is dict:
            args[0] = json.dumps(r_data)
        if not resource.startswith("/"):
            resource = "/" + resource
        resource = self._host + resource.replace("//", "/")
        resp = getattr(rest, method)(resource, *args, **kwargs)
        if resp.getcode() > 299 or resp.getcode() < 200:
            raise ResponseError(resp)
        return Response(resp)

    def post(self, resource, request_data, **kwargs):
        return self.__method__(resource, request_data, **kwargs)
        
    def get(self, resource, **kwargs):
        return self.__method__(resource, **kwargs)

    def put(self, resource, request_data, **kwargs):
        return self.__method__(resource, request_data, **kwargs)

    def delete(self, resource, **kwargs):
        return self.__method__(resource, **kwargs)

    def patch(self, resource_url, data, **kwargs):
        return self.__method__(resource, request_data, **kwargs)

