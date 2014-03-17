from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ClientEndpoint

class TopHashProtocol(Protocol):
    def connectionMade(self):
        print "Connection Made"

    def dataReceived(self, data):
        self.transport.loseConnection()
        print "Received data: \n", data

    def sendMessage(self, msg):
        print "SendMessage: ", msg
        self.transport.write(msg)

class TopHashFactory(Factory):
    def buildProtocol(self, addr):
        return TopHashProtocol()

def gotProtocol(p):
    print "Got Protocol"
    p.sendMessage("5")

if __name__ == '__main__':
    point = TCP4ClientEndpoint(reactor, "localhost", 8000)
    d = point.connect(TopHashFactory())
    d.addCallback(gotProtocol)
    reactor.run()
