---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.6.0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Custom HTTP Hander

Python の HTTP サーバーの練習を Jupyter Notebook 上で完結させる.
`multiprocessing.Process` を利用してセルを実行するたびにサーバーを立ち上げるプロセス作り直すことにする.
こうすることでポート番号を使いまわすことができる.


# References:

- 
掌田 津耶乃 著 [Pythonフレームワーク
Flaskで学ぶWebアプリケーションのしくみとつくり方](https://www.socym.co.jp/book/1224) 出版: ソシム株式会社
  - 簡易的な HTTP サーバーの書き方はここを参考にした. いきなり Flask, Django に触る前にこの本を読むべき

- https://docs.python.org/ja/3/library/multiprocessing.html

```python
# Import modules
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
proc = None # 以降のセルでプロセスを指す識別子として活用する
```

```python
# Import modules for Jupyter Notebook
from IPython.display import display, HTML
```

```python
def init_server(port):
    HTTPServer(
        ("", port), CustomHTTPHander
    ).serve_forever()

port = 8000
```

`self.wfile.write(...)` の中身をいじって次のセルを繰り返し実行してみよ.

```python
class CustomHTTPHander(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h1>Hello World</h1>")


if proc is not None:
    # 前のセルで定義されているプロセスを終了する.
    print("Terminate")
    proc.terminate()

proc = Process(
    target=init_server, args=(port, ), daemon=True
)
proc.start()

display(HTML(f"""
<iframe src="http://localhost:{port}/index.html" width="800" height="100"></iframe>
"""))
```
