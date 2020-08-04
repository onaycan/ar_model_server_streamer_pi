from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import ssl

httpd = HTTPServer(('10.42.0.1', 5000), SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket,  
certfile='./certs/server.pem', server_side=True)
print("socket there")

httpd.serve_forever()

print("serving")
