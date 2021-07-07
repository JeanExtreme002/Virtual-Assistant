import socket

def get_private_ip():
    return socket.gethostbyname(socket.gethostname())
