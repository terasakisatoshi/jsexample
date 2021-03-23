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
from flask import Flask
from multiprocessing import Process
proc = None
```

```python
from IPython.display import display, HTML
```

```python
app = Flask("main")

@app.route("/")
def index():
    return "<h1>Flask app</h1>"




if proc is not None:
    print(f"Terminate {proc}")
    proc.terminate()

port = 5000
proc = Process(
    target=app.run, 
    kwargs=dict(host="localhost", port=port),
    daemon=True,
)

proc.start()

display(HTML(f"""
<iframe src="http://localhost:{port}/" width="500" height="100"></iframe>
"""))
```
