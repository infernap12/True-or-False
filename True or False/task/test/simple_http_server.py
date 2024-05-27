"""
A simple HTTP Server
"""

import base64
import json
import logging
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from random import choice, seed

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.StreamHandler(sys.stdout))

PORT = 8000
ToF_USERNAME = "rihanna"
ToF_PASSWORD = "785bdf267c5244"
memory = []

questions = [
    {
        "question": "Rihanna is a rugby player",
        "answer": "False"
    },
    {
        "question": "The heaviest land mammal is the African bush elephant",
        "answer": "True"
    },
    {
        "question": "Finback whale is the largest whale",
        "answer": "False"
    },
    {
        "question": "Sperm whale has the biggest brain have ever existed",
        "answer": "True"
    },
    {
        "question": "John Bardeen - Walter Brattain - William Shockley invented the first working transistors at Bell Labs",
        "answer": "True"
    },
    {
        "question": "Bright brothers had invented the first successful airplane",
        "answer": "False"
    },
    {
        "question": "The World Wide Web was invented in CERN",
        "answer": "True"
    },
    {
        "question": "Illidan Stormrage betrayed his own clan",
        "answer": "True"
    },
    {
        "question": "The first mechanical computer - The Babbage Difference Engine - was designed by Charles Babbage in 1922",
        "answer": "False"
    },
    {
        "question": "Pong is the first commercially successful video game",
        "answer": "True"
    },
    {
        "question": "The International Space Station circles the globe every 900 minutes",
        "answer": "False"
    },
    {
        "question": "The Sun is 109 times wider than Earth",
        "answer": "True"
    },
]


class CustomHandler(BaseHTTPRequestHandler):
    seed(9876543210)

    def log_message(self, format_, *args):
        pass

    def do_GET(self):
        if self.path == "/download/file.txt":
            self._download()
        elif self.path == "/login":
            self._login()
        elif self.path == "/game":
            self._game()
        elif self.path == "/health":
            self._serve_code_msg(200, "Server is running!")
        else:
            self._serve_default()

    def _download(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.send_header('Content-Disposition', 'attachment; filename="file.txt"')
        self.end_headers()
        with open(file="./test/file.txt", mode='rb') as file:
            self.wfile.write(file.read())

    def _login(self):
        logger.debug(msg=f"{self.headers.keys()}")
        logger.debug(msg=f"{self.headers.values()}")

        auth = self.headers.get("Authorization")

        try:
            username, password = base64.b64decode(auth.split()[-1]) \
                .decode(encoding="utf-8") \
                .split(":") \
                if auth else (None, None)

        except Exception as err:
            print(err.__class__.__name__, err.__str__())
            username, password = None, None

        if username and password and \
                username == ToF_USERNAME and \
                password == ToF_PASSWORD:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Set-Cookie", "username=rihanna")

            self.end_headers()
            self.wfile.write("Logged in successfully!\n".encode())

        else:
            self._serve_code_msg(401, "Wrong username or password!")

    def _game(self):
        logger.debug(msg=f"{self.headers.keys()}")
        logger.debug(msg=f"{self.headers.values()}")

        auth = self.headers.get("Cookie")

        try:
            _, username = auth.split("=") if auth else (None, None)
        except Exception as err:
            print(err.__class__.__name__, err.__str__())
            username = None

        if username and username == ToF_USERNAME:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            question = choice(questions)
            while question in memory[-5:]:
                question = choice(questions)
            memory.append(question)

            self.wfile.write(json.dumps(question).encode())

        else:
            self._serve_code_msg(401, "Please login first!")

    def _serve_default(self):
        logger.debug(msg=f"{self.request}")
        logger.debug(msg=f"{self.headers.keys()}")
        logger.debug(msg=f"{self.headers.values()}")

        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        with open(file='./test/index.html', mode='rb') as file:
            self.wfile.write(file.read())

    def _serve_code_msg(self, code, message):
        self.send_response(code)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f'{message}\n'.encode())

    do_POST = do_GET


def simple_server():
    srv = HTTPServer(('', PORT), CustomHandler)
    logger.log(level=logging.DEBUG, msg=f"Server started on port {PORT}")
    srv.serve_forever()


if __name__ == '__main__':
    simple_server()
