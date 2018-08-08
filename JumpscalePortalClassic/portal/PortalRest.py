from jumpscale import j
from . import exceptions
from . import Validators
import urllib.request
import urllib.parse
import urllib.error
import requests
import re


class PortalRest():

    def __init__(self, webserver):
        self.ws = webserver
        self.logger = j.logger.get("j.portal.tools")

    def validate(self, auth, ctx):
        if ctx.params == "":
            msg = 'No parameters given to actormethod.'
            ctx.start_response('400 Bad Request', [])
            return False, msg
        if auth and ctx.env['beaker.session']['user'] == 'guest':
            msg = 'NO VALID AUTHORIZATION KEY GIVEN, use get param called key (check key probably auth error).'
            ctx.start_response('401 Unauthorized', [])
            return False, msg

        def emptyisnone(func):
            def wrapper(val):
                if val == '':
                    return None
                else:
                    return func(val)
            return wrapper

        NoneType = type(None)
        convertermap = {'int': ((int, NoneType), emptyisnone(j.data.types.int.fromString)),
                        'float': ((float, int, NoneType), emptyisnone(j.data.types.float.fromString)),
                        'str': ((str, NoneType), emptyisnone(str)),
                        'bool': ((bool, NoneType), emptyisnone(j.data.types.bool.fromString))
                        }
        params = self.ws.routes[ctx.path]['params']

        def loadList(key):
            if isinstance(ctx.params[key], (list, NoneType)):
                return
            try:
                ctx.params[key] = j.data.types.list.fromString(ctx.params[key])
            except ValueError:
                raise exceptions.BadRequest('Value of param %s not correct needs to be of type %s' % (key, param['type']))

        for key, param in params.items():
            is_default = False
            if key not in ctx.params or ctx.params[key] in ('', None):
                if param['optional']:
                    # means is optional
                    if param['tags'].labelExists('default_is_none'):
                        ctx.params[key] = None
                        continue
                    ctx.params[key] = param['default']
                    is_default = True
                else:
                    raise exceptions.BadRequest('Param with name:%s is missing.' % key)
            if param['type'] in convertermap:
                type_, converter = convertermap[param['type']]
                if not isinstance(ctx.params[key], type_):
                    try:
                        ctx.params[key] = converter(ctx.params[key])
                    except ValueError:
                        raise exceptions.BadRequest('Value of param %s not correct needs to be of type %s' % (key, param['type']))
            elif param['type'] == 'list':
                loadList(key)
            elif param['type'] in ['list(int)', 'list(bool)', 'list(float)', 'list(str)']:
                if not ctx.params[key] is None:
                    loadList(key)
                    m = re.search("list\((?P<type>\w+)\)", param['type'])
                    if m:
                        type_, converter = convertermap[m.group('type')]
                        for i in range(len(ctx.params[key])):
                            try:
                                if not isinstance(ctx.params[key][i], type_):
                                    ctx.params[key][i] = converter(ctx.params[key][i])

                            except ValueError:
                                raise exceptions.BadRequest('Value of param %s not correct needs to be of type %s' % (key, param['type']))

            if not is_default:
                if param['tags'].tagExists('validator'):
                    validator_name = param['tags'].tagGet('validator').upper()
                    validator = getattr(Validators, validator_name)

                    if isinstance(validator, str):
                        def validator_callable(val):
                            m = re.match(validator, val)
                            return m and m.end() == len(val)
                    else:
                        validator_callable = validator

                    if not validator_callable(ctx.params[key]):
                        raise exceptions.BadRequest('Value of param %s is not a valid %s' % (key, validator_name.lower()))

                if param['tags'].tagExists('validator-max'):
                    validator_max = int(param['tags'].tagGet('validator-max'))
                    if param['type'] == 'str':
                        if len(ctx.params[key]) > validator_max:
                            raise exceptions.BadRequest("Length of param %s should be smaller than %d" % (key, validator_max))
                    if param['type'] in ('int', 'float'):
                        if ctx.params[key] > validator_max:
                            raise exceptions.BadRequest("Value of param %s should be smaller than %d" % (key, validator_max))

                if param['tags'].tagExists('validator-min'):
                    validator_min = int(param['tags'].tagGet('validator-min'))
                    if param['type'] == 'str':
                        if len(ctx.params[key]) < validator_min:
                            raise exceptions.BadRequest("Length of param %s should be larger than %d" % (key, validator_min))
                    if param['type'] in ('int', 'float'):
                        if ctx.params[key] < validator_min:
                            raise exceptions.BadRequest("Value of param %s should be larger than %d" % (key, validator_min))

        return True, ""

    def restPathProcessor(self, path):
        """
        Function which parse a path, returning True or False depending on
        successfull parsing, a error message and a dict of parameters.
        When successfull the params dict contains the path elements otherwise it
        contains if provided the actorname  and appname.
        """
        # self.logger.info("Process path %s" % path, 9)
        params = {}
        while path != "" and path[0] == "/":
            path = path[1:]
        while path != "" and path[-1] == "/":
            path = path[:-1]
        if path.strip() == "":
            return (False, "Bad input path was empty. Format of url need to be http://$ipaddr/rest/$appname/$actorname/$actormetho?...", {})
        paths = path.split("/")
        if len(paths) < 3:
            msginfo = "Format of url need to be http://$ipaddr/rest/$appname/$actorname/$actormethod?...\n\n"
            if len(paths) > 0:
                appname = paths[0]
            else:
                appname = ""
                actor = ""
            if len(paths) > 1:
                actor = paths[1]
            else:
                actor = ""
            params["appname"] = appname
            params["actorname"] = actor
            return (False, msginfo, params)
        params["paths"] = paths
        return (True, "", params)

    def restextPathProcessor(self, path):
        self.logger.info("Process path %s" % path, 9)
        params = {}
        while path != "" and path[0] == "/":
            path = path[1:]
        while path != "" and path[-1] == "/":
            path = path[:-1]
        if path.strip() == "":
            return (False, "Bad input path was empty. Format of url need to be http://$ipaddr/restext/$appname/$modelname/$args", {})
        paths = path.split("/")
        if len(paths) < 2:
            msginfo = "Format of url need to be http://$ipaddr/restext/$appname/$modelname/$args...\n\n"
            if len(paths) > 0:
                appname = paths[0]
            else:
                appname = ""
                modelname = ""
            if len(paths) > 1:
                modelname = paths[1]
            else:
                modelname = ""
            params["appname"] = appname
            params["modelname"] = modelname
            return (False, msginfo, params)
        params["paths"] = paths
        return (True, "", params)

    def restRouter(self, env, start_response, path, paths, ctx, ext=False, routekey=None, human=False):
        """
        does validaton & authorization
        returns right route key
        """
        if not routekey:
            routekey = "%s_%s_%s" % (paths[0], paths[1], paths[2])
        # self.logger.info("Execute %s %s" % (env["REMOTE_ADDR"], routekey))
        routes = self.ws.routes
        if routekey not in routes:
            self.activateActor(paths[0], paths[1])
        if routekey not in routes:
            routekey = "%s_%s" % (ctx.env['REQUEST_METHOD'], routekey)
        if routekey in routes:
            if human:
                ctx.fformat = "human"
            elif("format" not in ctx.params):
                ctx.fformat = routes[routekey]['returnformat']
            else:
                ctx.fformat = ctx.params["format"]
            ctx.path = routekey
            ctx.fullpath = path
            ctx.application = paths[0]
            ctx.actor = paths[1]
            ctx.method = paths[2]
            auth = routes[routekey]['auth']

            resultcode, msg = self.validate(auth, ctx)  # validation & authorization (but user needs to be known)
            if resultcode is False:
                if human:
                    params = {}
                    params["error"] = "Incorrect Request: %s" % msg
                    params["appname"] = ctx.application
                    params["actorname"] = ctx.actor
                    params["method"] = ctx.method
                    page = self.ws.pageprocessor.returnDoc(ctx, start_response, "system",
                                                           "restvalidationerror", extraParams=params)
                    return (False, ctx, [str(page)])
                else:
                    return (False, ctx, msg)
            else:
                return (True, ctx, routekey)
        else:
            msg = "Could not find method, path was %s" % (path)
            appname = paths[0]
            actor = paths[1]
            contentType, data = self.ws.pageprocessor.reformatOutput(ctx, msg, restreturn=not human)
            ctx.start_response("404 Not Found", [('Content-Type', contentType)])
            if human:
                page = self.getServicesInfo(appname, actor)
                return (False, ctx, self.ws.pageprocessor.raiseError(ctx=ctx, msg=msg, msginfo=str(page)))
            else:
                contentType, data = self.ws.pageprocessor.reformatOutput(ctx, msg, restreturn=False)
                return (False, ctx, data)

    def execute_rest_call(self, ctx, routekey, ext=False):
        routes = self.ws.routes
        try:
            method = routes[routekey]['func']
            result = method(ctx=ctx, **ctx.params)
            return (True, result)
        except requests.exceptions.ConnectionError as error:
            message = error.args[0]
            raise exceptions.Error(message)
        except Exception as errorObject:
            eco = j.errorhandler.processPythonExceptionObject(errorObject)
            msg = "Execute method %s failed." % (routekey)
            return (False, self.ws.pageprocessor.raiseError(ctx=ctx, msg=msg, errorObject=eco))

    def processor_rest(self, env, start_response, path, human=True, ctx=False):
        """
        orignal rest processor (get statements)
        e.g. http://localhost/restmachine/system/contentmanager/notifySpaceModification?name=www_openvstorage&authkey=1234
        """
        if ctx is False:
            raise RuntimeError("ctx cannot be empty")
        try:
            # self.logger.info("Routing request to %s" % path, 9)

            def respond(contentType, msg):
                # self.logger.info("Responding %s" % msg, 5)
                if contentType:
                    ctx.start_response('200 OK', [('Content-Type', contentType)])
                # print msg
                return msg

            success, msg, params = self.restPathProcessor(path)
            if not success:
                params["error"] = msg
                if human:
                    page = self.ws.pageprocessor.returnDoc(ctx, start_response, "system", "rest",
                                                           extraParams=params)
                    return [str(page)]
                else:
                    httpcode = "404 Not Found"
                    contentType, data = self.ws.pageprocessor.reformatOutput(ctx, msg, restreturn=True)
                    ctx.start_response(httpcode, [('Content-Type', contentType)])
                    return data
            paths = params['paths']

            success, ctx, routekey = self.restRouter(env, start_response, path,
                                                     paths, ctx, human=human)
            if not success:
                # in this case routekey is really the errormsg
                return routekey

            success, result = self.execute_rest_call(ctx, routekey)
            if not success:
                return result

            if human:
                ctx.format = "json"
                params = {}
                params["result"] = result
                return [str(self.ws.pageprocessor.returnDoc(
                    ctx, start_response, "system", "restresult", extraParams=params))]
            else:
                contentType, result = self.ws.pageprocessor.reformatOutput(ctx, result)
                return respond(contentType, result)
        except Exception as errorObject:
            eco = j.errorhandler.processPythonExceptionObject(errorObject)
            if ctx is False:
                print("NO webserver context yet, serious error")
                eco.process()
                print(eco)
            else:
                return self.ws.pageprocessor.raiseError(ctx, errorObject=eco)

    def processor_restext(self, env, start_response, path, human=True, ctx=False):
        """
        rest processer gen 2 (not used by the original get code)
        """
        if ctx is False:
            raise RuntimeError("ctx cannot be empty")
        try:
            self.logger.info("Routing request to %s" % path, 9)

            def respond(contentType, msg):
                if contentType:
                    start_response('200 OK', [('Content-Type', contentType)])
                return msg

            success, message, params = self.restextPathProcessor(path)

            if not success:
                params["error"] = message
                if human:
                    page = self.ws.pageprocessor.returnDoc(ctx, start_response, "system", "rest",
                                                           extraParams=params)
                    return [str(page)]
                else:
                    return self.ws.pageprocessor.raiseError(ctx, message)
            requestmethod = ctx.env['REQUEST_METHOD']
            paths = params['paths']
            appname = paths[0]
            model = paths[1]
            objectid = None
            if len(paths) > 2:
                objectid = int(paths[2])
                ctx.params['id'] = objectid

            osiscl = j.clients.osis.getCategory(self.ws.osis, appname, model)
            osismap = {'GET': ['get', 'list', 'search'], 'POST': [''], 'DELETE': ['delete']}

            if requestmethod == 'GET':
                result = self._handle_get(ctx, osiscl, objectid)
            elif requestmethod in ('POST', 'PUT'):
                result = self._handle_post(ctx, osiscl, objectid)
            elif requestmethod == 'DELETE':
                result = self._handle_delete(ctx, osiscl, objectid)
            else:
                start_response('405 Method not allowed', [('Content-Type', 'text/html')])
                return 'Requested method is not allowed'

            if human:
                ctx.fformat = "json"
                params = {}
                params["result"] = result
                return [str(self.ws.pageprocessor.returnDoc(
                    ctx, start_response, "system", "restresult", extraParams=params))]
            else:
                ctx.fformat = 'jsonraw'
                contentType, result = self.ws.pageprocessor.reformatOutput(ctx, result)
                return respond(contentType, result)
        except Exception as errorObject:
            eco = j.errorhandler.processPythonExceptionObject(errorObject)
            if ctx is False:
                print("NO webserver context yet, serious error")
                eco.process()
                print(eco)
            else:
                return self.ws.pageprocessor.raiseError(ctx, errorObject=eco)

    def _handle_get(self, ctx, osiscl, objectid):
        if objectid:  # get object
            result = osiscl.get(objectid)
            return result.dump()
        else:  # list or search
            if ctx.env['QUERY_STRING']:  # search
                query = self._get_query_string(ctx)
                return osiscl.search(query)[1:]
            else:  # list
                return osiscl.search({})[1:]

    def _handle_delete(self, ctx, osiscl, objectid):
        return osiscl.delete(objectid)

    def _handle_post(self, ctx, osiscl, objectid):
        fields = ctx.params
        if objectid:  # update
            obj = osiscl.get(objectid)
        else:  # new
            obj = osiscl.new()
        if 'id' in fields:
            fields.pop('id')
        for field, value in fields.items():
            setattr(obj, field, value)
        return osiscl.set(obj)

    def _get_query_string(self, ctx):
        fields = dict()
        if ctx.env['QUERY_STRING']:
            queryparts = ctx.env['QUERY_STRING'].split('&')
            for querypart in queryparts:
                querypart = urllib.parse.unquote(querypart)
                field, value = querypart.split('=')
                fields[field] = int(value) if value.isdigit() else value
        return fields

    def activateActor(self, appname, actor):
        if not "%s_%s" % (appname, actor) in list(self.ws.actors.keys()):
            # need to activate
            try:
                result = self.ws.actorsloader.getActor(appname, actor)
            except Exception as e:
                eco = j.errorhandler.processPythonExceptionObject(e)
                eco.process()
                print(eco)
                return False
            if result is None:
                # there was no actor
                return False
