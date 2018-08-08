from jumpscale import j

from JumpscalePortalClassic.PortalBase import *


class PortalRootClassFactory:

    portal_instance = None

    def __init__(self):
        self.__jslocation__ = "j.portal.tools"
        self.logger = j.logger.get("j.portal.tools")
        self._codegentools = None
        self._specparser = None
        self._models = None
        self._datatables = None
        self._defmanager = None
        self._docgenerator = None
        self._macrohelper = None
        self._portalloaders = None
        self._infomgr = None
        self._html = None
        self._docpreprocessor = None
        self._swaggerGen = None
        self._taskletengine = None
        self._server = None
        self._usermanager = None
        # self._portal = None

    @property
    def codegentools(self):
        from JumpscalePortalClassic.tools.codegentools.codegentools import codegentools
        if self._codegentools is None:
            self._codegentools = codegentools()
        return self._codegentools

    @property
    def usermanager(self):
        from JumpscalePortalClassic.tools.usermanager.UserManager import UserManager
        if self._usermanager is None:
            self._usermanager = UserManager()
        return self._usermanager

    @property
    def specparser(self):
        from JumpscalePortalClassic.tools.specparser.specparser import specparser
        if self._specparser is None:
            self._specparser = specparser()
        return self._specparser

    @property
    def models(self):
        from JumpscalePortalClassic.data.models.Models import models
        if self._models is None:
            self._models = models()
        return self._models

    @property
    def datatables(self):
        from JumpscalePortalClassic.portal.datatables.datatables import datatables
        if self._datatables is None:
            self._datatables = datatables()
        return self._datatables

    @property
    def defmanager(self):
        from JumpscalePortalClassic.portal.defmanager.defmanager import defmanager
        if self._defmanager is None:
            self._defmanager = defmanager()
        return self._defmanager

    @property
    def docgenerator(self):
        from JumpscalePortalClassic.portal.docgenerator.docgenerator import docgenerator
        if self._docgenerator is None:
            self._docgenerator = docgenerator()
        return self._docgenerator

    @property
    def macrohelper(self):
        from JumpscalePortalClassic.portal.macrohelper.macrohelper import macrohelper
        if self._macrohelper is None:
            self._macrohelper = macrohelper()
        return self._macrohelper

    @property
    def portalloaders(self):
        from JumpscalePortalClassic.portal.portalloaders.portalloaders import portalloaders
        if self._portalloaders is None:
            self._portalloaders = portalloaders()
        return self._portalloaders

    @property
    def infomgr(self):
        from JumpscalePortalClassic.portal.infomgr.infomgr import infomgr
        if self._infomgr is None:
            self._infomgr = infomgr()
        return self._infomgr

    @property
    def html(self):
        from JumpscalePortalClassic.portal.html.html import html
        if self._html is None:
            self._html = html()
        return self._html

    @property
    def docpreprocessor(self):
        from JumpscalePortalClassic.portal.docpreprocessor.DocPreprocessor import docpreprocessor
        if self._docpreprocessor is None:
            self._docpreprocessor = docpreprocessor()
        return self._docpreprocessor

    @property
    def swaggergen(self):
        from JumpscalePortalClassic.tools.swaggergen.swaggergen import swaggergen
        if self._swaggergen is None:
            self._swaggergen = swaggergen()
        return self._swaggergen

    @property
    def taskletengine(self):
        from JumpscalePortalClassic.tools.taskletengine.taskletengine import taskletengine
        if self._taskletengine is None:
            self._taskletengine = taskletengine()
        return self._taskletengine
    
    @property
    def server(self):
        from JumpscalePortalClassic.portal.PortalServerFactory import PortalServerFactory
        if self._server is None:
            self._server = PortalServerFactory()
        return self._server

    # @property
    # def server(self):
    #     from JumpscalePortalClassic.portal.server import server
    #     if self._server is None:
    #         self._server = server()
    #     return self._server

    def _getBaseClass(self):
        return PortalBase

    def _getBaseClassLoader(self):
        return PortalBaseLoader
