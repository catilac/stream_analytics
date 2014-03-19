import tornado.ioloop
from tornado.web import RequestHandler, Application
import sys
import os
import json

curr_dir = os.path.dirname(__file__)

path = os.path.abspath(os.path.join(curr_dir, '../lib'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

import top_hashtag

th_client = None

class IndexHandler(RequestHandler):
    def get(self):
        self.write("Stub for index page")

class TopHashHandler(RequestHandler):
    def get(self, num):
        if not th_client:
            th_client = top_hashtag.TopHashtagClient()
        top_hashtags = th_client.get_top_n(num)
        resp = json.dumps(top_hashtags)
        self.write(resp)

if __name__ == '__main__':
    settings = {
        'static_path': os.path.join(curr_dir, 'static')
    }

    application = Application([
        (r"/", IndexHandler),
        (r"/top/([0-9]+)/?", TopHashHandler),
    ], settings)

    application.listen(3001)
    print "Web Running on port 3001"
    tornado.ioloop.IOLoop.instance().start()
