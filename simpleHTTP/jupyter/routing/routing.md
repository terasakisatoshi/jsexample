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

# HTTP Server を用いたルーティングの理解

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
class CustomHTTPHander(BaseHTTPRequestHandler):
    def do_GET(self):
        _url = urlparse(self.path)
        router = {
            "/":self.index,
            "/another":self.another,
        }
        rfunc = router.get(_url.path, self.error)
        rfunc()
        
    def index(self):
        self.send_response(200)
        self.end_headers()
        with open("index.html", 'r') as f:
            file = f.read()
        html = file.format(
            title = "MyTitle",
            message = "Hi from message",
        )
        self.wfile.write(html.encode("utf-8"))
        return None
    def another(self):
        self.send_response(200)
        self.end_headers()
        with open("another.html", 'r') as f:
            file = f.read()
        html = file.format(
            title="Another",
            message = "Hi from message in Another",
            data = '{\n data: "this is data"\n}'
        )
        self.wfile.write(html.encode("utf-8"))
        return None
    def error(self):
        self.send_error(404, "NOT FOUND")
        return None
    
def init_server(port):
    HTTPServer(
        ("", port), CustomHTTPHander
    ).serve_forever()


def start_server(port=8000):
    global proc
    if proc is not None:
        # 前のセルで定義されているプロセスを終了する.
        print("Terminate")
        proc.terminate()

    proc = Process(
        target=init_server, args=(port, ), daemon=True
    )
    proc.start()

    display(HTML(f"""
    <iframe src="http://localhost:{port}/" width="800" height="300"></iframe>
    """))
    
start_server()
```

```python

```
