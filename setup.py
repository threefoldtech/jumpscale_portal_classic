from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
import os
import collections

# zlib1g-dev/zesty
# libjpeg-dev/zesty


def _post_install(libname, libpath):
    from jumpscale import j

    # add this plugin to the config
    c = j.core.state.configGet('plugins', defval={})
    c[libname] = "%s/github/threefoldtech/jumpscale_portal_classic/JumpscalePortalClassic" % j.dirs.CODEDIR
    j.core.state.configSet('plugins', c)

    j.tools.jsloader.generate()



class install(_install):

    def run(self):
        _install.run(self)
        libname = self.config_vars['dist_name']
        libpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), libname)
        self.execute(_post_install, (libname, libpath), msg="Running post install task")


class develop(_develop):

    def run(self):
        _develop.run(self)
        libname = self.config_vars['dist_name']
        libpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), libname)
        self.execute(_post_install, (libname, libpath), msg="Running post install task")


long_description = ""
try:
    from pypandoc import convert
    long_description = convert("README.md", 'rst')
except ImportError:
    long_description = ""


setup(
    name='JumpscalePortalClassic',
    version='9.2.0',
    description='Automation framework for cloud workloads portal',
    long_description=long_description,
    url='https://github.com/threefoldtech/jumpscale_portal_classic',
    author='THreeFoldTech',
    author_email='info@threefold.tech',
    license='Apache',
    packages=find_packages(),
    install_requires=[
        'redis>=2.10.5',
        'colorlog>=2.10.0',
        'pytoml>=0.1.14',
        'ipython>=6.1.0',
        'colored_traceback',
        'pystache>=0.5.4',
        'libtmux>=0.7.3',
        'httplib2>=0.10.3',
        'netaddr>=0.7.19',
        'peewee>=2.10.1',
        'uvloop>=0.8.0',
        'paramiko>=2.2.3',  # for parallel-ssh
        'python-jose>=1.3.2',
        'watchdog>=0.8.3',
        'pymux>=0.13',
        'pyyaml',
        'ipdb>=0.10.3',
        'requests>=2.18.1',
        'cython',
        'pycapnp>=0.5.12',
        'path.py>=10.3.1',
        'pudb',
        'msgpack-python',
        'pyblake2',
        # 'mongoengine==0.10.6',
        'gevent',
        'beaker',
        'mimeparse',
        'flask',
        # 'flask-bootstrap',
    ],
    cmdclass={
        'install': install,
        'develop': develop,
        'developement': develop
    },
)
