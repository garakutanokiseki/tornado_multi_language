#!/usr/bin/env python
#   Sample main.py Tornado file
#
#   Author: Mike Dory
#       11.12.11
#
import os.path
import os
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
 
# import and define tornado-y things
from tornado.options import define, options
define("port", default=5000, help="run on the given port", type=int)
 
# application settings and handle mapping info
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ("/", MainHandler)
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)

# the main page
class MainHandler(tornado.web.RequestHandler):
    # XXX
    def get(self):
        # 強制的にローカルを設定する
        self.locale = tornado.locale.get('ja_JP')
        
        #テンプレートをレンダリングする
        self.render(
            "main.html",
            locale = self.locale.name,
            locales = tornado.locale.get_supported_locales(),
            )

# Main rootine
def main():
    options.parse_command_line()

    app = Application()
    app.listen(options.port)
    
    tornado.locale.load_translations(os.path.join(os.path.dirname(__file__), "translations"))

    # start it up
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()
