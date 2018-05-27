import sys
import config
from TCPServer.server import ThreadingSSLTCPServer, TCPHandler


def main():
    print("Starting server on {}:{} ...".format(config.HOST, config.PORT))
    server = ThreadingSSLTCPServer((config.HOST, config.PORT),
                                   TCPHandler,
                                   config.CERTFILE,
                                   config.KEYFILE)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()