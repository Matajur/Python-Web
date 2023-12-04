import json
import logging
import mimetypes
import socket
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path
from threading import Thread

BASE_DIR = Path().joinpath("front-init")
BUFFER = 1024
M_SERVER_IP = "0.0.0.0"
M_SERVER_PORT = 3000
S_SERVER_IP = "127.0.0.1"
S_SERVER_PORT = 5000
STATUS_OK = 200
STATUS_REDIRECT = 302
STATUS_NOT_FOUND = 404
STORAGE = Path().joinpath("storage/data.json")


class HTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        send_data_to_socket(body)
        self.send_response(STATUS_REDIRECT)
        self.send_header("Location", "/message.html")
        self.end_headers()

    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case "/":
                self.send_html(BASE_DIR.joinpath("index.html"))
            case "/message.html":
                self.send_html(BASE_DIR.joinpath("message.html"))
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html(BASE_DIR.joinpath("error.html"), STATUS_NOT_FOUND)

    def send_html(self, filename, status_code=STATUS_OK):
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())

    def send_static(self, filename):
        self.send_response(STATUS_OK)
        mime_type, *rest = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header("Content-Type", mime_type)
        else:
            self.send_header("Content-Type", "text/plain")
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())


def run(server=HTTPServer, handler=HTTPHandler):
    logging.info("Start server")
    server_address = (M_SERVER_IP, M_SERVER_PORT)
    http_server = server(server_address, handler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server stopped")
        http_server.server_close()


def run_socket_server(ip, port):
    logging.info("Start socket server")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    try:
        while True:
            data, address = server_socket.recvfrom(BUFFER)
            save_data(data)
    except KeyboardInterrupt:
        logging.info("Socket server stopped")
        server_socket.close()


def save_data(data):
    body = urllib.parse.unquote_plus(data.decode())
    try:
        payload = {
            key: value for key, value in [el.split("=", 1) for el in body.split("&", 1)]
        }

        with open(STORAGE, "r", encoding="utf-8") as file:
            content = json.load(file)
            content.update({str(datetime.now()): payload})

        with open(STORAGE, "w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False)

    except ValueError as err:
        logging.error(f"Faled parse data {body} with error: {err}")
    except OSError as err:
        logging.error(f"Faled write data {body} with error: {err}")


def send_data_to_socket(body):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(body, (S_SERVER_IP, S_SERVER_PORT))
    client_socket.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    if not STORAGE.exists():
        with open(STORAGE, "w", encoding="utf-8") as file:
            json.dump({}, file, ensure_ascii=False)

    thread_server = Thread(target=run)
    thread_server.start()

    thread_socket = Thread(target=run_socket_server, args=(S_SERVER_IP, S_SERVER_PORT))
    thread_socket.start()
