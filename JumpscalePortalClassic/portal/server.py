from jumpscale import j

base = j.portal.tools._getBaseClassLoader()


class server(base):

    def __init__(self):
        base.__init__(self)
