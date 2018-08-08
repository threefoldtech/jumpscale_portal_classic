from . import PortalServer

import time

from jumpscale import j


class Group():
    pass


class PortalServerFactory():

    def __init__(self):
        self.active = None
        self.__jslocation__ = "j.portal.servers"
        self.logger = j.logger.get("j.portal.servers")        
        # self.inprocess = False
        self.config = {}

    def get(self,path=""):
        if path=="":
            path = j.sal.fs.getcwd()
        configpath = "%s/config.toml"%path
        if not j.sal.fs.exists(configpath):
            raise RuntimeError("cannot find config file on %s"%configpath)
        C=j.tools.jinja2.template_render(configpath,IP="",DIRS=j.dirs.__dict__)
        self.config = j.data.serializer.toml.loads(C)
        return PortalServer.PortalServer()

    # def getPortalConfig(self, appname):
    #     cfg = j.sal.fs.joinPaths(j.dirs.base, 'apps', appname, 'cfg', 'portal')
    #     return j.config.getConfig(cfg)

    # def loadActorsInProcess(self, name='main'):
    #     """
    #     make sure all actors are loaded on j.apps...
    #     """
    #     class FakeServer(object):

    #         def __init__(self):
    #             self.actors = dict()
    #             self.epoch = time.time()
    #             self.actorsloader = j.portal.tools.portalloaders.portalloaderfactory.getActorsLoader()
    #             self.spacesloader = j.portal.tools.portalloaders.portalloaderfactory.getSpacesLoader()

    #         def addRoute(self, *args, **kwargs):
    #             pass

    #         def addSchedule1MinPeriod(self, *args, **kwargs):
    #             pass

    #         addSchedule15MinPeriod = addSchedule1MinPeriod

    #     self.inprocess = True
    #     # self._inited = False
    #     j.apps = Group()
    #     # basedir = j.sal.fs.joinPaths(j.dirs.cfgDir, 'portals', name)
    #     # hrd = j.data.hrd.get("%s/config.hrd" % basedir)
    #     appdir = hrd.get("param.cfg.appdir")
    #     appdir = appdir.replace("$base", j.dirs.base)
    #     j.sal.fs.changeDir(appdir)
    #     server = FakeServer()
    #     j.portal.tools.server.active = server
    #     server.actorsloader.scan(appdir)
    #     server.actorsloader.scan(basedir + "/base")

    #     for actor in list(server.actorsloader.actors.keys()):
    #         appname, actorname = actor.split("__", 1)
    #         try:
    #             server.actorsloader.getActor(appname, actorname)
    #         except Exception as e:
    #             print(("*ERROR*: Could not load actor %s %s:\n%s" % (appname, actorname, e)))
