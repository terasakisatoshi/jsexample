const http = require("http");
const fs = require("fs");
const ejs = require("ejs");
const url = require("url");
const qs = require("querystring");
const index_page = fs.readFileSync("index.ejs", "utf8");
const style_css = fs.readFileSync("./styles.css", "utf8");
const other_page = fs.readFileSync("./other.ejs", "utf8");
let server = http.createServer(getFromClient);

server.listen(3000);
console.log("Server Starts");

function response_index(request,response) {
    var msg = "This is a Index Page";
    var content = ejs.render(index_page, {
        title: "Index",
        content:msg,
    })
    response.writeHead(200, { "Content-Type": "text/html"});
    response.write(content);
    response.end();
}

function response_other(request,response) {
    var msg = "This is Other Page";

    if (request.method == "POST"){
        var body="";
        request.on("data", (data)=>{
            body+=data;
        });

        request.on('end', ()=>{
            var post_data = qs.parse(body);
            msg += " you wrote" + post_data.msg;
            var content = ejs.render(other_page,{
                title: "Other",
                content: msg,
            });
            response.writeHead(200, { "Content-Type": "text/html"});
            response.write(content);
            response.end();
        })
    }else{
        var msg = "Not found";
        var content = ejs.render(other_page,{
            title:"Other",
            content: msg,
        });
        response.writeHead(200, {"Content-Type": "text/html"});
        response.write(content);
        response.end();
    }

}

function getFromClient(request, response) {
    let url_parts = url.parse(request.url,true);
    switch (url_parts.pathname) {
        case "/":
            response_index(request, response);
            break;
        case "/other":
            response_other(request,response);
            break;
        default:
            response.writeHead(200, { "Content-Type": "text/plain" });
            response.end("No Page");
            break;
    }
}