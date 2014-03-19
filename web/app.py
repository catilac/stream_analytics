import tornado.ioloop
from tornado.web import RequestHandler, Application
import sys
import os
import json

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib'))
print path
if not path in sys.path:
    sys.path.insert(1, path)
del path
import top_hashtag

th_client = top_hashtag.TopHashtagClient()

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
