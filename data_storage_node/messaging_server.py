import socket
from messaging_client import MessagingClient
from leader_election import LeaderElection


class MessagingServer:
    server_socket: socket.socket
    client: MessagingClient
    leader_election: LeaderElection

    def __init__(self, ip: str, port: int):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen(1)

        self.client = MessagingClient()
        self.leader_election = LeaderElection()
        print(f"Server running on {ip}:{port}")

    def start(self):
        while True:
            connection, address = self.server_socket.accept()
            print(f"Connection from: {address}")

            data = connection.recv(1024).decode()
            if not data:
                continue

            self.handle_request(data)
            connection.close()

    def handle_request(self, data: str):
        print(f"Received data: {data}")
