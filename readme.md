# Python -tornado の多言語対応
## はじめに
tornadoは多言語対応しており簡単に多言語化することができます。  
多言語化は、辞書ファイルとなるcsvファイルを対応する言語分だけ用意することで対応できます。

## 翻訳用csvファイルの準備
翻訳時の辞書となるcsvは以下のように記載します。

```
英語, 翻訳語
```
この記事でのサンプルコードは以下となります。

ファイル名:en_US.csv
```
"Username", "Username"
"Password", "Password"
"Sign in", "Sign in"
```

ファイル名：ja.csv
```
Username, ユーザー名(ja)
Password, パスワード
Sign in, サインイン
```

## 多言語対応したテンプレートのファイルの準備
以下のテンプレートの例では、"Sign in"、"Username"、"Password"を多言語化しています。

```
<html>
   <head>
      <title>FriendFeed - {{ _("Sign in") }}</title>
   </head>
   <body>
     <form>
     {{ locale }}
       <div>{{ _("Username") }} <input type="text" name="username"/></div>
       <div>{{ _("Password") }} <input type="password" name="password"/></div>
       <div><input type="submit" value="{{ _("Sign in") }}"/></div>
      {% module xsrf_form_html() %}
     </form>
   </body>
 </html>
 ```
## メインプログラムの準備

```
#!/usr/bin/env python
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
        # 強制的にローカルを設定する場合は以下のようにします。
        #self.locale = tornado.locale.get('ja')

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
```

# 実行方法
以下のコマンドで実行します。
```
python main.py
```

以下のURLでブラウザから参照できます。
```
http://127.0.0.1:5000
```
