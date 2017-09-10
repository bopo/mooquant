# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import abc
import six

if sys.version < '3':
    import Queue as queue
    import cPickle as pickle
    from xmlrpclib import ServerProxy
    from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
else:
    import queue
    import pickle
    from xmlrpc.client import ServerProxy
    from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

# __all__ = (
#     'SimpleXMLRPCRequestHandler',
#     'SimpleXMLRPCServer',
#     'ServerProxy',
#     'pickle',
#     'queue',
# )
