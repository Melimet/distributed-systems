from time import time
from typing import List, Optional, Tuple
from config import id as node_id

from message_schemas import AckMessage, ElectionMessage, NodeRegistryMessage
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

    successor_ip: Optional[str]
    successor_port: Optional[int]

    leader_node_id: Optional[int]
    leader_node_ip: Optional[str]
    leader_node_port: Optional[int]
    leader_elected: bool

    messaging_client: MessagingClient

    def __init__(self):
        self.leader_elected = False
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

    async def register_node_and_update_successor(self):
        response = await self.messaging_client.send_to_reverse_proxy(
            NodeRegistryMessage.register().data
        )
        node_registry_message = NodeRegistryMessage(response.data)
        self.node_id = node_registry_message.get_id()
        self.successor_ip = node_registry_message.get_successor_ip()
        self.successor_port = node_registry_message.get_successor_port()

    async def start_leader_election(self):
        """
        Leader is elected with LCR algorithm. Any node can initiate the election.
        The node with the highest id will be elected as the leader.
        """
        self.leader_node_id = None
        self.leader_node_ip = None
        self.leader_node_port = None
        self.leader_elected = False
        await self.register_node_and_update_successor()
        await self.send_election_message(self.node_id)

    async def send_election_message(
        self, id: int, ip: Optional[str] = None, port: Optional[int] = None
    ):
        try:
            message = ElectionMessage.from_leader(id, ip, port)
            await self.messaging_client.send(
                self.successor_ip, self.successor_port, message.data
            )
        except:
            pass

    async def process_election_message(self, message: ElectionMessage):
        id = message.get_id()
        ip = message.get_ip()
        port = message.get_port()
        self.leader_elected = False

        # Need to verify successor to avoid infinite loop
        await self.register_node_and_update_successor()

        if id == HALT:
            print("Elected leader: ", self.leader_node_id)
            self.leader_elected = True
            if self.leader_node_id != self.node_id:
                await self.send_election_message(HALT)
            else:
                await self.messaging_client.send_to_reverse_proxy(
                    ElectionMessage.from_leader(self.node_id).data
                )
            return AckMessage.from_ack_message()

        if id < self.node_id:
            return AckMessage.from_ack_message()

        self.leader_node_id = id
        self.leader_node_ip = ip
        self.leader_node_port = port

        if id == self.node_id:
            await self.send_election_message(HALT)
            return AckMessage.from_ack_message()
        else:
            await self.send_election_message(id, ip, port)
            return AckMessage.from_ack_message()
