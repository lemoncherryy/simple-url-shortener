import json, time, sys
from http import server as httpserver
from socketserver import TCPServer as tcpserver
from datetime import datetime

class config_management:
    def __init__(self, config_file_location):
        f = open(config_file_location, "r")
        raw_data = f.read()
        print(raw_data)
        f.close()
        self.json_data = json.loads(raw_data)

    def destination(self, source):
        try:
            return self.json_data["links"][source]
        except KeyError:
            return self.json_data["failure_url"]

    def get_port(self):
        return self.json_data["port"]

    def get_host(self):
        return self.json_data["host"]


class redirect_handler(httpserver.SimpleHTTPRequestHandler):
    def set_config(self, config_class):
        self.config = config_class

    def do_GET(self):
        print(str(datetime.now()) + ": " + str(self.client_address) + " requested: " + self.path)
        self.send_response(301)
        self.send_header("Location", self.config.destination(self.path.lstrip("/")))
        self.end_headers()

class __main__:
    config = config_management(sys.argv[1])
    server_handler = redirect_handler
    server_handler.set_config(server_handler, config)
    web_server = tcpserver((config.get_host(), config.get_port()), server_handler)
    web_server.serve_forever()
