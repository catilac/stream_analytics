from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import threading

from top_hashtags import TopHashtags

top_hashtags = TopHashtags()
threading.Thread(target=top_hashtags.start).start()

class StatServer(Protocol):
    def __init__(self, factory, top_hashtags):
        self.factory = factory
        self._top_hashtags = top_hashtags

    def get_top(self, num):
        return self._top_hashtags.get_top_n(num)

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols+1
        print "CONNECT Num Connections is now: %d" % self.factory.numProtocols

    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols-1
        print "DISCONNECT Num Connections is now: %d" % self.factory.numProtocols

    def dataReceived(self, data):
        num = 15
        if data:
            try:
                num = int(data)
            except:
                print "Invalid input"

        top_hashtags = str(self.get_top(num))
        self.transport.write(top_hashtags)
        self.transport.loseConnection()

class StatFactory(Factory):
    def __init__(self):
        self.numProtocols = 0

    def buildProtocol(self, addr):
        """ Start TopHash and pass it into protocol """
        return StatServer(self, top_hashtags)

def main():
    endpoint = TCP4ServerEndpoint(reactor, 8000)
    endpoint.listen(StatFactory())
    print "Running Top Hash on port 8000"
    reactor.run()

if __name__ == '__main__':
    main()

