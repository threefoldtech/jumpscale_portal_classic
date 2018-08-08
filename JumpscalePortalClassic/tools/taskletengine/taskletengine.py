from jumpscale import j

base = j.portal.tools._getBaseClassLoader()


class taskletengine(base):

    def __init__(self):
        base.__init__(self)
