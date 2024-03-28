var http = require('http'); 
var server = http.createServer(function (req, res) {
    if (req.url == '/') { 
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.write('<html><body><h1 style="color:orange;">Welcome to Linh Website v0.1</h1></body></html>');
        res.end();
    }
    else if (req.url == "/training") {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.write('<html><body><h1 style="color:green;">Welcome to Training page v0.1!</h1></body></html>');
        res.end();
    }
    else if (req.url == "/admin") {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.write('<html><body><h1 style="color:black;">You need admin permission to access this page! -v0.1</h1></body></html>');
        res.end();
    }
    else
        res.end('Invalid Request! v0.1');
});
server.listen(5000);
console.log('Nodejs is running at port 5000...')