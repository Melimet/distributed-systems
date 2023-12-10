from time import time
from typing import List, Optional, Tuple
import argparse

from message_schemas import ElectionMessage
from messaging_client import MessagingClient

HALT = -1
ELECTION_TIMEOUT_MS = 5_000


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

    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    args = parser.parse_args()

    id = args.id

    nodes = [
        Node(0, "localhost", 5120),
        Node(1, "localhost", 5121),
        Node(2, "localhost", 5122),
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

    def get_successor(self) -> Node:
        successor_index = (self.node_id + 1) % len(self.nodes)
        return self.nodes[successor_index]

    def should_start_election(self) -> bool:
        if self.leader_elected:
            return False

        current_time = int(time() * 1000)
        return current_time - self.election_start > ELECTION_TIMEOUT_MS

    def start_leader_election(self):
        """
        Leader is elected with LCR algorithm. Any node can initiate the election.
        The node with the highest id will be elected as the leader.
        """
        # TODO: Fetch nodes from node registry. Needed for fault tolerance if node fails mid election.
        self.election_start = int(time() * 1000)
        self.leader_node_id = self.node_id
        self.leader_elected = False
        self.send_election_message(self.node_id)

    def send_election_message(self, id: int):
        try:
            successor = self.get_successor()
            message = ElectionMessage().from_id(id)
            self.messaging_client.send(successor.ip, successor.port, message.data)
        except:
            pass

    def receive_election_message(self, id: int):
        self.leader_elected = False

        if id == HALT:
            print("Elected leader: ", self.leader_node_id)
            self.leader_elected = True
            self.election_start = 0
            if self.leader_node_id != self.node_id:
                self.send_election_message(HALT)
            return

        if id < self.node_id:
            return

        if id == self.node_id:
            self.leader_node_id = self.node_id
            self.send_election_message(HALT)
            return

        self.leader_node_id = id
        self.send_election_message(id)
