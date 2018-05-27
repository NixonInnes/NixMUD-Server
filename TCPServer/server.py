import os
import ssl
from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler

from Auth import auth


class SSLTCPServer(TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self,
                 server_address,
                 handler,
                 certfile,
                 keyfile,
                 ssl_version=ssl.PROTOCOL_TLSv1,
                 bind_and_activate=True

    ):
        TCPServer.__init__(self, server_address, handler, bind_and_activate)

        if not os.path.isfile(certfile):
            raise FileNotFoundError(f'SSL certificate "{certfile}" file not found!')
        self.certfile = certfile
        if not os.path.isfile(keyfile):
            raise FileNotFoundError(f'SSL key "{keyfile}" not found!')
        self.keyfile = keyfile
        self.ssl_version = ssl_version

    def get_request(self):
        sock, addr = self.socket.accept()
        stream = ssl.wrap_socket(sock,
                                 server_side=True,
                                 certfile=self.certfile,
                                 keyfile=self.keyfile,
                                 ssl_version=self.ssl_version)
        return stream, addr


class ThreadingSSLTCPServer(ThreadingMixIn, SSLTCPServer):
    pass


class States(object):
    UNAUTH = 0x00
    RACE = 0x01
    CLASS = 0x02
    AUTHD = 0x04


class TCPHandler(BaseRequestHandler):
    states = States

    def setup(self):
        print(f'Connection received: {self.client_address}')
        self.user = None

    def handle(self):
        with open('Help/intro.txt', 'r') as f:
            welcome_msg = f.read()
        self.send(welcome_msg)
        self.state = self.states.UNAUTH
        while True:
            data = self.request.recv(1024)
            msg = data.decode('utf-8').strip()
            if not self.state is self.states.AUTHD:
                auth(self, msg)
            else:
                self.handler(msg)

    def send(self, msg):
        self.request.sendall(msg.encode('utf-8'))

    def disconnect(self):
        self.request.close()

    def __del__(self):
        if self.request:
            self.request.close()
