import asyncio
import socket
import select
from file_storage import FileStorage
from messaging_client import MessagingClient
from message_schemas import (
    AckMessage,
    ElectionMessage,
    FileMessage,
    MessageType,
    Message,
    SyncMessage,
)
from leader_election import LeaderElection


class MessagingServer:
    client: MessagingClient
    leader_election: LeaderElection
    file_storage: FileStorage
    ip: str
    port: int

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.client = MessagingClient()
        self.leader_election = LeaderElection()
        self.file_storage = FileStorage()
        print(f"Server running on {ip}:{port}")

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.ip, self.port)
        asyncio.create_task(self.start_leader_election_if_needed())

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        data = await reader.read(1024)
        message = data.decode()

        response_message = await self.handle_request(message)
        writer.write(response_message.data.encode())
        await writer.drain()
        writer.close()

    async def handle_request(self, data: str) -> Message:
        message = Message(data)

        if message.get_type() == MessageType.ELECTION:
            return await self.leader_election.process_election_message(
                ElectionMessage(data)
            )

        elif message.get_type() == MessageType.FILE:
            return await self.file_storage.process_file_message(
                FileMessage(data), self.leader_election
            )

        elif message.get_type() == MessageType.SYNC:
            return self.file_storage.synchronize_follower(
                SyncMessage(data), self.leader_election
            )

        elif message.get_type() == MessageType.HEARTBEAT:
            return AckMessage.from_ack_message()

    async def start_leader_election_if_needed(self):
        while not self.leader_election.leader_elected:
            await self.leader_election.start_leader_election()
            await asyncio.sleep(5)
