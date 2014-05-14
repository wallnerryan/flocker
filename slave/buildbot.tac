from twisted.application import service
from twisted.python.filepath import FilePath
from buildslave.bot import BuildSlave

basedir = FilePath(__file__).parent
rotateLength = 10000000
maxRotatedFiles = 10

# note: this line is matched against to check that this is a buildslave
# directory; do not edit it.
application = service.Application('buildslave')

from twisted.python.logfile import LogFile
from twisted.python.log import ILogObserver, FileLogObserver
logfile = LogFile.fromFullPath(basedir.child("twistd.log").path, rotateLength=rotateLength,
                             maxRotatedFiles=maxRotatedFiles)
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

buildmaster_host = 'build.hybridcluster.net'
port = 9989
slavename = basedir.child('slave.name').getContent()
passwd = basedir.child('slave.passwd').getContent()
keepalive = 600
usepty = False
umask = 0022
maxdelay = 300

s = BuildSlave(buildmaster_host, port, slavename, passwd, basedir,
               keepalive, usepty, umask=umask, maxdelay=maxdelay,
               allow_shutdown=False)
s.setServiceParent(application)
