from jumpscale import j

base = j.portal.tools._getBaseClassLoader()


class macrohelper(base):

    def __init__(self):
        base.__init__(self)
