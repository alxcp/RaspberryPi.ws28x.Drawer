from http.server import BaseHTTPRequestHandler, HTTPServer


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        raise NotImplementedError()


def server_thread(target_port):
    server_address = ('', target_port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    port = 8000
    print("Starting server at port %d" % port)
    server_thread(port)
