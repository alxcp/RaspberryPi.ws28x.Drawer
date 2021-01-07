from http.server import BaseHTTPRequestHandler, HTTPServer

html = '''<html>
              <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
                 .button_led {display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
              </style>
              <body>
                 <h2>Hello from the Raspberry Pi!</h2>
                 <p><a href="/led/on"><button class="button button_led">Led ON</button></a></p>
                 <p><a href="/led/off"><button class="button button_led">Led OFF</button></a></p>
              </body>
            </html>'''

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET request, Path:", self.path)
        if self.path == "/" or self.path.endswith("/led/on") or self.path.endswith("/led/off"):
            if self.path.endswith("/led/on"):
                print("led_pin, True")
            if self.path.endswith("/led/off"):
                print("led_pin, False")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))

def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    port = 8000
    print("Starting server at port %d" % port)
    #raspberrypi_init()
    server_thread(port)
    #raspberrypi_cleanup()
