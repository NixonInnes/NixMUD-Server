import os

# TCPServer Address
HOST = 'localhost'
PORT = 8000

# SSL Certificate Locations
CERTFILE = os.environ['CERTFILE']
KEYFILE = os.environ['KEYFILE']

# Database Address
DATABASE = 'sqlite:///database.sqlite'
