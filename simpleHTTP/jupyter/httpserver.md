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

# Jupyter 上で Web 開発

Webアプリを動かす際ににターミナルを開いてサーバーを立ち上げるスクリプトを呼び出すでしょ？あれってめんどくさくない？ それを管理するための領域を画面に占めたくない．Jupyter 上でサーバーの立ち上げをコントロールさせればいいのでは？なるほど．そんなあなたにこのノートブックを授けよう．


# References:

- 
掌田 津耶乃 著 [Pythonフレームワーク
Flaskで学ぶWebアプリケーションのしくみとつくり方](https://www.socym.co.jp/book/1224) 出版: ソシム株式会社
  - 簡易的な HTTP サーバーの書き方はここを参考にした. いきなり Flask, Django に触る前にこの本を読むべき

- https://docs.python.org/3/library/threading.html


## 準備

<!-- #region -->
このノートブックと同階層に `index.html` という名前の HTML スクリプトがあることを仮定する.

```html
<!DOCTYPE html>
<html>

<head>
  <title> Simple HTTP Server </title>
</head>

<body>
  <h1> Hello World </h1>
</body>

</html>
```

作ったことを確認するために `cat` コマンドで `index.html` の中身を見てみよう.
<!-- #endregion -->

```python
!cat index.html
```

さてこのHTMLを表示するウェブアプリを動かしたい. が，その前にこの `index.html` がどのような表示になるかをざっくり確認しよう.

```python
# Import modules for Jupyter Notebook
from IPython.display import display, HTML
```

```python
display(HTML(
"""
    <!DOCTYPE html>
<html>

<head>
  <title> Simple HTTP Server </title>
</head>

<body>
  <h1> Hello World </h1>
</body>

</html>
"""
))

```

デカデカと Hello World という文字が出たら成功である. さて Jupyter で HTTP サーバーを立ち上げるようにしたい. サーバーを起動する(デーモン)スレッドを作る．ポートの重複を避けるために起動するごとに違うポートを使うことにするという方針をとる.

```python
# Import modules
from http.server import SimpleHTTPRequestHandler, HTTPServer
import random
import threading
```

```python
# 一回だけ実行せよ
current_candidates = list(range(8000,8888))
```

```python
port = random.choice(current_candidates)
current_candidates.remove(port) #
print(f"port={port}")

def init_server():
    HTTPServer(
        ('', port), SimpleHTTPRequestHandler
    ).serve_forever()
    
t = threading.Thread(target=init_server)
t.setDaemon(True)
t.start()

display(HTML(
f"""
<iframe src="http://localhost:{port}/index.html" width="800" height="100"></iframe>
"""
))
```

デカデカと Hello World ができればOK
