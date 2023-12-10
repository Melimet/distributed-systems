import socket
import threading


class MessagingClient:
    client_socket = socket.socket

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, ip: str, port: int, message: str):
        self.client_socket.connect((ip, port))
        self.client_socket.send(message.encode())


class MessagingServer:
    server_socket: socket.socket

    def __init__(self, ip: str, port: int, client: MessagingClient):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen(1)
        self.client = client
        print(f"Server running on {ip}:{port}")

    def start(self):
        threading.Thread(target=self._start_server, daemon=True).start()

    def handle_request(self, data: str):
        print(f"Received data: {data}")

    def _start_server(self):
        while True:
            connection, address = self.server_socket.accept()
            print(f"Connection from: {address}")

            data = connection.recv(1024).decode()
            if not data:
                continue

            self.handle_request(data)
            connection.close()
