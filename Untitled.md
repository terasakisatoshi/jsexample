---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.10.3
  kernelspec:
    display_name: JavaScript
    language: javascript
    name: jslab
---

```javascript
var server = null;

const http = require("http");

if(server === null){
    server.close()
}
server = http.createServer(
    (request, response) => {
        response.end("<h1>Hello Node.js!</h1>");
    }
);

server.listen(3000)
```

```javascript

```
