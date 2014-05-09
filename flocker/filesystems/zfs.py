# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""
ZFS APIs.
"""

from __future__ import absolute_import

import os
from collections import namedtuple

from zope.interface import implementer

from twisted.internet.endpoints import ProcessEndpoint, connectProtocol
from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred
from twisted.internet.error import ConnectionDone, ProcessTerminated

from .interfaces import IFilesystemSnapshots
from ..snapshots import SnapshotName


class CommandFailed(Exception):
    """
    The ``zfs`` command failed for some reasons.
    """



class BadArguments(Exception):
    """
    The ``zfs`` command was called with incorrect arguments.
    """



class _AccumulatingProtocol(Protocol):
    """
    Accumulate all received bytes.
    """

    def __init__(self):
        self._result = Deferred()
        self._data = b""


    def dataReceived(self, data):
        self._data += data


    def connectionLost(self, reason):
        if reason.check(ConnectionDone):
            self._result.callback(self._data)
        elif reason.check(ProcessTerminated) and reason.value.exitCode == 1:
            self._result.errback(CommandFailed())
        elif reason.check(ProcessTerminated) and reason.value.exitCode == 2:
            self._result.errback(BadArguments())
        else:
            self._result.errback(reason)
        del self._result



def zfsCommand(reactor, arguments):
    """
    Run the ``zfs`` command-line tool with the given arguments.

    :param reactor: A ``IReactorProcess`` provider.

    :param arguments: A ``list`` of ``bytes``, command-line arguments to ``zfs``.

    :return: A :class:`Deferred` firing with the bytes of the result (on
        exit code 0), or errbacking with :class:`CommandFailed` or
        :class:`BadArguments` depending on the exit code (1 or 2).
    """
    endpoint = ProcessEndpoint(reactor, b"zfs", [b"zfs"] + arguments, os.environ)
    d = connectProtocol(endpoint, _AccumulatingProtocol())
    d.addCallback(lambda protocol: protocol._result)
    return d



class Filesystem(namedtuple("Filesystem", "pool")):
    """
    A ZFS filesystem.

    For now the goal is simply not to pass bytes around when referring to a
    filesystem.  This will likely grow into a more sophisticiated
    implementation over time.

    :attr pool: The filesystem's pool name, e.g. ``b"hpool/myfs"``.
    """



#@implementer(IFilesystemSnapshots)
class ZFSSnapshots(object):
    def __init__(self, reactor, filesystem):
        self._reactor = reactor
        self._filesystem = filesystem


    def create(self, name):
        encodedName = b"%s@%s" % (self._filesystem.pool, name.toBytes())
        d = zfsCommand(self._reactor, [b"snapshot", encodedName])
        d.addCallback(lambda _: None)
        return d


    def list(self):
        """
        Snapshots whose names cannot be decoded are presumed not to be related
        to Flocker, and therefore will not be included in the result.
        """
        d = zfsCommand(self._reactor,
                       [b"list", b"-H", b"-r", b"-t", b"snapshot", b"-o",
                        b"name", b"-s", b"name", self._filesystem.pool])
        def parseSnapshots(data):
            result = []
            for line in data.splitlines():
                pool, encodedName = line.split(b'@', 1)
                if pool == self._filesystem.pool:
                    try:
                        result.append(SnapshotName.fromBytes(encodedName))
                    except ValueError:
                        pass
            return result
        d.addCallback(parseSnapshots)
        return d
