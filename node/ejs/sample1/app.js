const http = require("http");
const fs = require("fs");
const ejs = require("ejs");
const url = require("url");

const index_page = fs.readFileSync("index.ejs", "utf8");
const style_css = fs.readFileSync("./styles.css", "utf8");
let server = http.createServer(getFromClient);

server.listen(3000);
console.log("Server Starts");

function getFromClient(request, response) {
    let url_parts = url.parse(request.url);
    switch (url_parts.pathname) {
        case "/":
            let content = ejs.render(index_page, {
                title: "Index",
                content: "root",
            });
            response.writeHead(200, {
                "Content-Type": "text/html",
            })
            response.write(content);
            response.end();
            break;
        case "/styles.css":
            response.writeHead(200, { "Content-Type": "text/css" });
            response.write(style_css);
            response.end();
            break;
        default:
            response.writeHead(200, { "Content-Type": "text/plain" });
            response.end("No Page");
            break;
    }

}