from effects.registry import PixelEffectsRegistry
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from drawers.console_drawer import ConsoleDrawer
# from drawers.adafruit_neopixel_drawer import NeoPixelDrawer

html = '''<html>
              <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
                 .button_led {display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 90px; margin: 2px; cursor: pointer;}
              </style>
              <body>
                 <p><a href="/led/on"><button class="button button_led">Led ON</button></a></p>
                 <p><a href="/led/off"><button class="button button_led">Led OFF</button></a></p>
                 <p><a href="/next/effect"><button class="button button_led">Next effect</button></a></p>
                 <p>Effect name: {effect_name}</p>
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
            start_drawer(self, pixel_effects, drawer_thread)
        elif self.path.endswith("/led/off"):
            print("led_pin, False")
            pixel_effects.stop()
            drawer_daemon.join()
            drawer.clear()
        elif self.path.endswith("/next/effect"):
            pixel_effects.stop()
            drawer_daemon.join()
            drawer.clear()
            start_drawer(self, pixel_effects, drawer_next_effect)
        elif self.path == "/":
            print("home page")
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.replace('{effect_name}', pixel_effects.current_effect.get_name()).encode('utf-8'))


def server_thread(target_port):
    server_address = ('', target_port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


def drawer_thread(effects_registry):
    print('drawer thread started')
    effects_registry.play()


def drawer_next_effect(effects_registry):
    print('next effect')
    effects_registry.play_next_effect()


def start_drawer(self, effects_registry, function):
    self.drawer_daemon = threading.Thread(target=function, args=[effects_registry], daemon=True)
    self.drawer_daemon.start()


if __name__ == '__main__':
    # drawer = NeoPixelDrawer(100)
    drawer = ConsoleDrawer(100)
    pixel_effects = PixelEffectsRegistry(drawer)
    drawer_daemon = threading.Thread(target=drawer_thread, args=[pixel_effects], daemon=True)
    drawer_daemon.start()

    port = 8000
    print("Starting server at port %d" % port)

    server_thread(port)
