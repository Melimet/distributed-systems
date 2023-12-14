import socket
import select
from messaging_client import MessagingClient
from message_schemas import ElectionMessage, MessageType, Message
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
            if self.leader_election.should_start_election():
                self.leader_election.start_leader_election()

            self.check_incoming_messages()

    def check_incoming_messages(self):
        readable, _, _ = select.select([self.server_socket], [], [], 0)
        if not readable:
            return

        connection, address = self.server_socket.accept()
        print(f"Connection from: {address}")

        data = connection.recv(1024).decode()
        if not data:
            return

        self.handle_request(data)
        connection.close()

    def handle_request(self, data: str):
        print(f"Received data: {data}")
        message = Message(data)

        if message.get_type() == MessageType.ELECTION:
            message = ElectionMessage(data)
            self.leader_election.receive_election_message(message.get_id())
