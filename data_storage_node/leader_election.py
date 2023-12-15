from time import time
from typing import List, Optional, Tuple
from config import id as node_id

from message_schemas import AckMessage, ElectionMessage
from messaging_client import MessagingClient

HALT = -1


class Node:
    id: int
    ip: str
    port: int

    def __init__(self, id: int, ip: str, port: int):
        self.id = id
        self.ip = ip
        self.port = port


def get_nodes() -> Tuple[int, List[Node]]:
    """
    TODO: Get nodes from node registry.
    """
    id = node_id
    nodes = [
        Node(0, "storage0", 5120),
        Node(1, "storage1", 5121),
        Node(2, "storage2", 5122),
    ]

    return id, nodes


class LeaderElection:
    node_id: int
    nodes: List[Node]

    leader_node_id: int
    leader_elected: bool
    election_start: int
    messaging_client: MessagingClient

    def __init__(self):
        id, nodes = get_nodes()
        self.node_id = id
        self.nodes = nodes

        self.leader_node_id = id
        self.leader_elected = False
        self.election_start = 0
        self.messaging_client = MessagingClient()

    def is_leader(self) -> bool:
        return self.leader_elected and self.leader_node_id == self.node_id

    def get_successor(self) -> Node:
        successor_index = (self.node_id + 1) % len(self.nodes)
        return self.nodes[successor_index]

    def get_leader(self) -> Node:
        for node in self.nodes:
            if node.id == self.leader_node_id and self.leader_elected:
                return node
        return None

    async def start_leader_election(self):
        """
        Leader is elected with LCR algorithm. Any node can initiate the election.
        The node with the highest id will be elected as the leader.
        """
        # TODO: Fetch nodes from node registry. Needed for fault tolerance if node fails mid election.
        self.election_start = int(time() * 1000)
        self.leader_node_id = self.node_id
        self.leader_elected = False
        await self.send_election_message(self.node_id)

    async def send_election_message(self, id: int):
        try:
            successor = self.get_successor()
            message = ElectionMessage.from_id(id)
            await self.messaging_client.send(successor.ip, successor.port, message.data)
        except:
            pass

    async def process_election_message(self, message: ElectionMessage):
        id = message.get_id()
        self.leader_elected = False

        if id == HALT:
            print("Elected leader: ", self.leader_node_id)
            self.leader_elected = True
            self.election_start = 0
            if self.leader_node_id != self.node_id:
                await self.send_election_message(HALT)
            return AckMessage.from_ack_message()

        if id < self.node_id:
            return AckMessage.from_ack_message()

        if id == self.node_id:
            self.leader_node_id = self.node_id
            await self.send_election_message(HALT)
            return AckMessage.from_ack_message()

        self.leader_node_id = id
        await self.send_election_message(id)
        return AckMessage.from_ack_message()
