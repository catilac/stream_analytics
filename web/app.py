import tornado.ioloop
from tornado.web import RequestHandler, Application
import json

class IndexHandler(RequestHandler):
    def get(self):
        self.write("Stub for index page")

class TopHashHandler(RequestHandler):
    def get(self, num):
        resp = "The num is: %s" % num
        self.write(resp)

if __name__ == '__main__':
    application = Application([
        (r"/", IndexHandler),
        (r"/top/([0-9]+)/?", TopHashHandler),
    ])

    application.listen(3001)
    print "Web Running on port 3001"
    tornado.ioloop.IOLoop.instance().start()
