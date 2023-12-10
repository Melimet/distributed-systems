import socket


class MessagingClient:
    client_socket = socket.socket

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, ip: str, port: int, message: str):
        self.client_socket.connect((ip, port))
        self.client_socket.send(message.encode())
