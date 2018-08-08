# this must be in the beginning so things are patched before ever imported by other libraries
from gevent import monkey

monkey.patch_socket()
monkey.patch_ssl()
monkey.patch_thread()
monkey.patch_time()

from jumpscale import j


if __name__ == '__main__':

    server = j.portal.servers.get()
    server.start()

