# -*- mode:python; coding: utf-8 -*-

"""
API
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any common modules
import os
import odict
import shutil
import tempfile
import urlparse
import itertools

__all__ = ['SleipnirMapper', 'SleipnirAuth']

# Import here local required modules
from restfulie.api       import BaseAPI, BaseMapper
from restfulie.auth      import OAuthMixin
from restfulie.client    import Client
from restfulie.processor import auth_chain
from restfulie.services  import Services

# import here local submodules
TMPDIR = '/var/tmp'
try:
    from sleipnir.frontends.handset import constants
    TMPDIR = constants.__tmp_dir__
except ImportError:
    pass


#pylint: disable-msg=W0232
class Sleipnir(Client):
    """Base client class for Sleipnir API"""

    # When scaling, it's probably a good idea to split oauth and api
    # servers
    BASE_URL = "http://api.sleipnir-project.com"

    # Service Map
    TARGETS = {
        'apiv1': 'sleipnir-apiv1',
        'oauth': 'sleipnir-oauth',
    }

    def __init__(self, credentials=None):
        # Set default  urls for service
        print self.BASE_URL
        self.override_server(self.BASE_URL)
        # Finish instantiation
        Client.__init__(self, credentials)

    @classmethod
    def _override_service(cls, service, url, path=None, secure=False):
        """
        Use this class method to set sanity values for class
        properties when a custom server must be used
        """
        # Parse url; pylint:disable-msg=W0212,E1101
        url = urlparse.urlparse(url)
        assert url.netloc and url.scheme
        url = odict.odict(itertools.izip(url._fields, url))

        # Override class urls
        if path:
            url['path'] = path
        if secure:
            url['scheme'] = 'https'

        # Register
        urls = Services.get_instance().URLS
        urls[service] = urlparse.urlunparse(url.itervalues())

    @classmethod
    def override_server(cls, url, override_api=True, override_oauth=True):
        """Define URLS for api targets"""

        if override_api and 'apiv1' in cls.TARGETS:
            service = cls.TARGETS['apiv1']
            cls._override_service(service, url, path='/1')
        if override_oauth and 'oauth' in cls.TARGETS:
            cls._override_service(service, url, path='/oauth', secure=True)

    @classmethod
    def override_ca_certs(cls, services=None, locations=None, inline=None):
        """Override ca-certfiles from tornado with a custom cas"""

        def read_files(locs):
            """Fetch pem files from firt level dirs"""

            pem_dirs = itertools.ifilter(os.path.isdir, locs)
            pem_dirs = itertools.imap(os.listdir, pem_dirs)
            # Fetch files
            pem_file = itertools.ifilterfalse(os.path.isdir, locs)
            # Open it; pylint: disable-msg=W0142
            for path in itertools.chain(pem_file, *pem_dirs):
                # Only process One dir level
                try:
                    with open(path, 'r') as source:
                        yield source.read()
                except IOError:
                    pass

        # pylint: disable-msg=W0106
        os.path.exists(TMPDIR) or os.makedirs(TMPDIR, mode=0755)
        crt = tempfile.NamedTemporaryFile(dir=TMPDIR)

        if locations:
            ca_pems = itertools.imap("{0}\n".format, read_files(locations))
            crt.writelines(ca_pems)
        if inline:
            ca_pems = itertools.imap("{0}\n".format, inline)
            crt.writelines(ca_pems)
        crt.seek(0)

        # Get services that will be overrided by cacerts
        keys = services or cls.TARGETS.itervalues()
        assert isinstance(keys, (list, tuple))

        # Register cacert
        ca_files   = [os.path.join(TMPDIR, key) for key in keys]
        copy_files = itertools.izip([crt.name] * len(keys), ca_files)

        # Copy; pylint: disable-msg=W0106
        [shutil.copyfile(src, dst) for src, dst in copy_files]
        cacerts = Services.get_instance().CACERTS
        cacerts.update(itertools.izip(keys, ca_files))


#pylint: disable-msg=W0223, R0903
class SleipnirAuth(OAuthMixin):
    """ oauth method """

    # Base Url. OAuthMixin use target directly to resolve agaist
    # Services singleton. We delegate service registration to Client
    # (Sleipnir) object, in this case
    SERVICE = "sleipnir-oauth"

    # Auth mechanism implemented
    implements = "sleipnir"


# pylint: disable-msg=R0903
class SleipnirMapper(BaseMapper):
    """Mapper to make rest invokations more pythonic"""

    # pylint: disable-msg=R0903
    class SleipnirAPI(BaseAPI):
        """Extend BaseAPI class with custom values"""

        # Base Url. In this case we use
        TARGET  = "apiv1"

        # Our api is json based only
        FLAVORS = ["json"]

        # define default timeouts
        CONNECT_TIMEOUT = 5
        REQUEST_TIMEOUT = 10

    # pylint: disable-msg=R0903
    class SleipnirAuthAPI(SleipnirAPI):
        """Extense SleipnirAPI to sort chain on auth flows"""

        CHAIN = auth_chain

    # Register defined classes
    BASE_API = SleipnirAPI
    AUTH_API = SleipnirAuthAPI
