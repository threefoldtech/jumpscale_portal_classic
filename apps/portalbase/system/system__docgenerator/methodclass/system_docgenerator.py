from jumpscale import j
from JumpscalePortalClassic.portal import exceptions

INMAP = {'post': 'formData', 'get': 'query'}

INPUTMAP = {'bool': {'type': 'boolean'},
            'str': {'type': 'string'},
            'string': {'type': 'string'},
            'int': {'type': 'integer'},
            'float': {'type': 'number'},
            'list': {'type': 'string'},
            'dict': {'type': 'string'},
            }

RETURNMAP = {'bool': {'type': 'boolean'},
             'str': {'type': 'string'},
             'string': {'type': 'string'},
             'int': {'type': 'integer'},
             'float': {'type': 'number'},
             'list': {'$ref': '#/definitions/strarray'},
             'dict': {'$ref': '#/definitions/object'},
             }


class system_docgenerator(j.tools.code.classGetBase()):

    def __init__(self):
        self._te = {}
        self.actorname = "docgenerator"
        self.appname = "system"

    def getDocForActor(self, actorname, spec, hide_private_api):
        paths = spec['paths']
        tags = spec['tags']
        apppart, actorpart = actorname.split('__')
        # force load
        j.portal.tools.server.active.actorsloader.getActor(apppart, actorpart)
        specobj = j.portal.tools.specparser.specparserfactory.getactorSpec(apppart, actorpart, False)
        if not specobj:
            return
        tags.append({'name': actorname, 'description': specobj.description})
        for method in specobj.methods:
            if hide_private_api and method.tags and 'hide' in method.tags:
                continue
            methods = dict()
            path = '/%s/%s/%s' % (specobj.appname, specobj.actorname, method.name)
            methodtags = j.data.tags.getObject(method.tags)
            paths[path] = methods
            methodtypes = ('post', )
            if 'method' in methodtags.tags:
                methodtypes = [tag for tag in methodtags.tags['method'].split(',') if tag]
            for methodtype in methodtypes:
                methodinfo = dict()
                methods[methodtype] = methodinfo
                methodinfo['description'] = method.description
                methodinfo['tags'] = [actorname]
                resulttype = 'str'
                if method.result:
                    resulttype = method.result.type
                methodinfo['responses'] = {'200': {"description": "result",
                                                   "schema": RETURNMAP.get(resulttype, RETURNMAP['string'])
                                                   }
                                           }
                methodinfo['summary'] = method.description
                methodinfo['operationId'] = "%s_%s" % (methodtype, path.replace('/', '_'))
                if method.vars:
                    parameters = list()
                    methodinfo['parameters'] = parameters
                    for var in method.vars:
                        tagobj = j.data.tags.getObject(var.tags or '')
                        parameter = {'name': var.name, 'in': INMAP[methodtype],
                                     'description': var.description,
                                     'required': not tagobj.labelExists('optional'),
                                     }
                        parameter.update(INPUTMAP.get(var.ttype, INPUTMAP['string']))
                        if var.defaultvalue is not None:
                            parameter['default'] = var.defaultvalue
                        parameters.append(parameter)

    def prepareCatalog(self, **args):
        catalog = {'swagger': '2.0', 'basePath': '/restmachine/', 'paths': {}, 'tags': list()}
        catalog['info'] = {'description': '',
                           'version': '7.0',
                           'title': 'Jumpscale Actors',
                           }
        catalog['definitions'] = {'strarray': {'type': 'array', 'items': {'type': 'string'}},
                                  'intarray': {'type': 'array', 'items': {'type': 'integer'}},
                                  'object': {"type": "object",
                                             "additionalProperties": {"type": "string"}}}
        hide_private_api = args.get('skip_private')
        if 'actors' in args and args['actors']:
            actors = args['actors'].split(',')
        else:
            actors = j.portal.tools.server.active.getActors()

        if 'group' in args and args['group']:
            group = args['group']
            groups = dict()
            for actor in actors:
                group_name = actor.split('__')[0]
                groups.setdefault(group_name, []).append(actor)

            if group in groups.keys():
                actors = groups[group]
            else:
                raise exceptions.BadRequest("invalid actor group")

        for actor in sorted(actors):
            try:
                self.getDocForActor(actor, catalog, hide_private_api)
            except Exception as e:
                catalog['info']['description'] += "<p class='alert alert-danger'>Failed to load actor %s error was %s</p>" % (actor, e)
        return catalog
