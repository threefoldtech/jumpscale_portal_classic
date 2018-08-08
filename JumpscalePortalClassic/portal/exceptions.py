from jumpscale import j
import requests
import json
from functools import wraps
import http.client

codemapping = http.client.responses.copy()
codemapping[419] = 'Authentication Timeout'


class BaseError(BaseException):

    def __init__(self, code, headers, msg, status=None):
        self.code = code
        self.headers = headers
        self.msg = msg
        if status is None:
            status = codemapping.get(code, 'Unkonwn')
        self.status = status


class Error(BaseError):
    CODE = 500

    def __init__(self, msg, content_type='application/json'):
        if content_type == 'application/json':
            msg = json.dumps(msg)
        BaseError.__init__(self, self.CODE, [('Content-Type', content_type)], msg)


class Redirect(BaseError):

    def __init__(self, location):
        headers = [('Location', location)]
        BaseError.__init__(self, 302, headers, "")


class BadRequest(Error):
    CODE = 400


class Unauthorized(Error):
    CODE = 401


class Forbidden(Error):
    CODE = 403


class NotFound(Error):
    CODE = 404


class MethodNotAllowed(Error):
    CODE = 405


class Conflict(Error):
    CODE = 409


class PreconditionFailed(Error):
    CODE = 412


class AuthenticationTimeout(Error):
    CODE = 419


class ServiceUnavailable(Error):
    CODE = 503


class InternalServer(Error):
    CODE = 500


def catcherrors(debug=False, msg="Error was {}", ):
    def wrapper(method):
        @wraps(method)
        def mymeth(self, *methargs, **methkwargs):
            try:
                res = method(self, *methargs, **methkwargs)
            except requests.exceptions.HTTPError as e:
                headers = (('content-type', 'text/plain'),)
                if debug:
                    jsonresp = e.response.json()
                    if 'error' in jsonresp:
                        raise BaseError(e.response.status_code, headers, msg.format(jsonresp['error']))
                    else:
                        raise BaseError(e.response.status_code, headers, msg.format(str(e)))
                else:
                    raise BaseError(e.response.status_code, headers, msg.format(str(e)))
            except (requests.exceptions.ConnectionError, ConnectionError):
                raise ServiceUnavailable("Can't connect to robot server")
            except Exception as e:
                raise InternalServer(str(e))
            else:
                return res
        return mymeth
    return wrapper
