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
from urllib.parse import urlparse, parse_qs

proc = None # 以降のセルでプロセスを指す識別子として活用する
```

```python
# Import modules for Jupyter Notebook
from IPython.display import display, HTML
import ipywidgets as widgets
from ipywidgets import interact
```

```python
def init_server(port):
    HTTPServer(
        ("", port), CustomHTTPHander
    ).serve_forever()
```

```python
!cat index.html
```

<!-- #region -->
# `index.html` を呼び出す.

```python
with open("index.html", 'r') as f:
    indexfile = f.read()
```

のようにして `index.html` を読み込み，読み込んだ結果 `indexfile` を `utf-8` にエンコードしてやれば良い.

```python
indexfile.encode("utf-8")
```
<!-- #endregion -->

```python
class CustomHTTPHander(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        with open("index.html", 'r') as f:
            indexfile = f.read()
        self.wfile.write(indexfile.encode("utf-8"))

port = 8000

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

# Template を使う場合

Hello World という文字列はそろそろ見飽きてたのではないでしょうか？
HTML サーバーが返却する HTML を Python で制御しましょう. `template.html` というファイルを用意しているのでそれを読み込んでテンプレートを補完すれば良い.

```python
# title とか header1 とか paragraph の部分を Python で補完する.
!cat template.html
```

```python
class CustomHTTPHander(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        with open("template.html", 'r') as f:
            template = f.read()
        html = template.format(
            title = "MyTitle",
            header1 = "Header1",
            paragraph = "This is a paragraph",
        )
        self.wfile.write(html.encode("utf-8"))

port = 8001

if proc is not None:
    # 前のセルで定義されているプロセスを終了する.
    print("Terminate")
    proc.terminate()

proc = Process(
    target=init_server, args=(port, ), daemon=True
)
proc.start()

display(HTML(f"""
<iframe src="http://localhost:{port}/template.html" width="800" height="100"></iframe>
"""))
```

<!-- #region -->
# クエリーパラメータを使う

上記のセルにある下記のスニペットを使うことで `template.html` をベースとした HTML を構築することがわかった.

```python
html = template.format(
    title = "MyTitle",
    header1 = "Header1",
    paragraph = "This is a paragraph",
)
```

ただし，このままだとフィールド(`title`, `header`, `paragraph` などのこと) はハードコーディングされていて制御できない.
そこでクエリーパラメータを用いてHTMLの出力を制御する方針をとる.
<!-- #endregion -->

```python
class CustomHTTPHander(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        self.send_response(200)
        self.end_headers()

        title = query.get("title", ["DefaultTitle"])[0]
        header1 = query.get("header1", ["DefaultHeader1"])[0]
        paragraph = query.get("paragraph", ["DefaultParagraph"])[0]

        with open("template.html", 'r') as f:
            template = f.read()
        html = template.format(
            title = title,
            header1 = header1,
            paragraph = paragraph,
        )
        self.wfile.write(html.encode("utf-8"))

port = 8001

if proc is not None:
    # 前のセルで定義されているプロセスを終了する.
    print("Terminate")
    proc.terminate()

proc = Process(
    target=init_server, args=(port, ), daemon=True
)
proc.start()

 
title = widgets.Text(
    value='Title',
    placeholder='title',
    description='title:',
)

header1 = widgets.Text(
    value='Header1',
    placeholder='header1',
    description='header1:',
)

paragraph = widgets.Text(
    value='Paragraph',
    placeholder='paragraph',
    description='paragraph:',
)

def do(title, header1, paragraph):
    display(HTML(f"""
    <iframe src="http://localhost:{port}/template.html?title={title}&header1={header1}&paragraph={paragraph}" width="800" height="200"></iframe>
    """))
    
interact(do, title=title, header1=header1, paragraph=paragraph)
```
