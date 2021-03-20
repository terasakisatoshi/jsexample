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

```python
# Import modules
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from urllib.parse import urlparse, parse_qs
from cgi import FieldStorage

proc = None  # 以降のセルでプロセスを指す識別子として活用する
```

```python
!cat index.html
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

```python
class CustomHTTPHander(BaseHTTPRequestHandler):
    def do_GET(self):
        _url = urlparse(self.path)
        router = {
            "/": self.index,
            "/result": self.result
        }
        rfunc = router.get(_url.path, self.error)
        rfunc()

    def do_POST(self):
        form = FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
            }
        )
        value = form["textfield"].value
        self.send_response(200)
        self.end_headers()
        with open("form_result.html", 'r') as f:
            file = f.read()
        html = file.format(
            title="Result",
            message="Form Result",
            data=value,
        )
        self.wfile.write(html.encode("utf-8"))
        return None

    def index(self):
        self.send_response(200)
        self.end_headers()
        with open("index.html", 'r') as f:
            file = f.read()
        html = file.format(
            title="Hello",
            message="Send Form",
        )
        self.wfile.write(html.encode("utf-8"))
        return None

    def result(self):
        self.send_response(200)
        self.end_headers()
        with open("form_result.html", 'r') as f:
            file = f.read()
        html = file.format(
            title="Another",
            message="Hi from message in Another",
            data='{\n data: "this is data"\n}'
        )
        self.wfile.write(html.encode("utf-8"))
        return None

    def error(self):
        self.send_error(404, "NOT FOUND")
        return None

def main():
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
    <iframe src="http://localhost:{port}/" width="800" height="200"></iframe>
    """))
    
main()
```
