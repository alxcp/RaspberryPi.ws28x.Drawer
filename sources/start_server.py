import board
import neopixel
import time
import colorsys
import random
import os,sys
import effects.registry

import effects.different
import effects.matrix
import effects.watch
import effects.fire
import effects.meteor_rain

from drawers.base import DrawerBase

from helpers.color_rgb import ColorRGB

from helpers.timeouts import Timeout
from effects.registry import PixelEffectsRegistry
from datetime import timedelta, datetime, date, time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from drawers.adafruit_neopixel_drawer import NeoPixelDrawer

html = '''<html>
              <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
                 .button_led {display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 90px; margin: 2px; cursor: pointer;}
              </style>
              <body>
                 <p><a href="/led/on"><button class="button button_led">Led ON</button></a></p>
                 <p><a href="/led/off"><button class="button button_led">Led OFF</button></a></p>
                 <p><a href="/next/effect"><button class="button button_led">Next effect</button></a></p>
              </body>
            </html>'''

class ServerHandler(BaseHTTPRequestHandler):
    
    drawer = None
    pixel_effects = None
    drawer_daemon = None

    
    def do_GET(self):
        print("GET request, Path:", self.path)

        if self.path.endswith("/led/on"):                
            print("led_pin, True")             
            start_drawer(self, drawer, pixel_effects, drawer_thread)
        elif self.path.endswith("/led/off"):
            print("led_pin, False")
            drawer.stop()
            drawer_daemon.join()
            drawer.clear()
        elif self.path.endswith("/next/effect"):
            drawer.stop()
            drawer_daemon.join()
            drawer.clear()
            start_drawer(self, drawer, pixel_effects, drawer_next_effect)
        elif self.path == "/":
            print ("home page")
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))
            return
                
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    
def drawer_thread(drw, eff):
    print ('drawer thread started')
    eff.play_effect(effects.meteor_rain.MeteorRainEffect(drw))
    
def drawer_next_effect(drw, eff):
    print ('next effect')
    eff.next_effect()

def start_drawer(self, drw, eff, fun):
    self.drawer_daemon = threading.Thread(target=fun, args=(drw, eff), daemon=True)
    self.drawer_daemon.start()
   

if __name__ == '__main__':
    drawer = NeoPixelDrawer(300)
    pixel_effects = PixelEffectsRegistry(drawer)
    drawer_daemon = threading.Thread(target=drawer_thread, args=(drawer, pixel_effects), daemon=True)
    drawer_daemon.start()
    
    port = 8000
    print("Starting server at port %d" % port)

    server_thread(port)
