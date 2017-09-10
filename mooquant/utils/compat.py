# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import abc
import six

if sys.version < '3':
    import Queue as queue
    from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
else:
    import queue
    from xmlrpc.server import SimpleXMLRPCServer

__all__ = (
    'SimpleXMLRPCRequestHandler',
    'SimpleXMLRPCServer',
    'queue',
)
