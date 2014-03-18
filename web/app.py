import tornado.ioloop
from tornado.web import RequestHandler, Application
import sys
import json

sys.path.append('../lib')
import top_hash

th_client = top_hash.TopHashClient()

class IndexHandler(RequestHandler):
    def get(self):
        self.write("Stub for index page")

class TopHashHandler(RequestHandler):
    def get(self, num):
        top_hashtags = th_client.get_top_n(num)
        resp = json.dumps(top_hashtags)
        self.write(resp)

if __name__ == '__main__':
    application = Application([
        (r"/", IndexHandler),
        (r"/top/([0-9]+)/?", TopHashHandler),
    ])

    application.listen(3001)
    print "Web Running on port 3001"
    tornado.ioloop.IOLoop.instance().start()
