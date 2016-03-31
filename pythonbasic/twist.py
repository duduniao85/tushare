#coding=utf-8
__author__ = 'xuyuming'
from twisted.internet import reactor
from twisted.internet.protocol import Protocol,Factory
from twisted.protocols.basic import  LineReceiver
# class SimpleLogger(Protocol):
#         def connectionMade(self):
#             print 'Got connection from ',self.transport.client #数据传输对象
#         def connectionLost(self, reason):
#             print self.transport.client,'disconnected'
#         def dataReceived(self, data):
#             print data
# factory = Factory()
# factory.protocol=SimpleLogger
#
# reactor.listenTCP(1234,factory)
# reactor.run()

class SimpleLogger(LineReceiver):
        def connectionMade(self):
            print 'Got connection from ',self.transport.client #数据传输对象
        def connectionLost(self, reason):
            print self.transport.client,'disconnected'
        def dataReceived(self, line):
            print line
factory = Factory()
factory.protocol=SimpleLogger

reactor.listenTCP(1234,factory)
reactor.run()

