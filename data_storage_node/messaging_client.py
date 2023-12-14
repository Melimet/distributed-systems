import socket


class MessagingClient:
    def __init__(self):
        pass

    def send(self, ip: str, port: int, message: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((ip, port))
            client_socket.sendall(message.encode())
