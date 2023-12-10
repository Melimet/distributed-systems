from typing import List, Tuple, Optional
import argparse

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
    TODO: Remove this and replace it with a RPC call to node registry.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    args = parser.parse_args()

    id = args.id
    nodes = [
        Node(0, "localhost", 5000),
        Node(1, "localhost", 5001),
        Node(2, "localhost", 5002),
    ]

    return id, nodes


class LeaderElection:
    node_id: int
    nodes: List[Node]

    leader_node_id: int
    leader_elected: bool
    messaging_client: MessagingClient

    def __init__(self):
        id, nodes = get_nodes()
        self.node_id = id
        self.nodes = nodes

        self.leader_node_id = id
        self.leader_elected = False
        self.messaging_client = MessagingClient()

    def get_successor(self) -> Node:
        successor_index = (self.node_id + 1) % len(self.nodes)
        return self.nodes[successor_index]

    def start_leader_election(self):
        """
        Leader is elected with LCR algorithm. Any node can initiate the election.
        The node with the highest id will be elected as the leader.
        """
        self.leader_node_id = self.node_id
        self.leader_elected = False
        self.send_election_message(self.node_id)

    def send_election_message(self, id: int):
        # TODO: send message to successor
        #       should retry if successor does not respond
        #       should get new successor if current successor fails
        successor = self.get_successor()
        self.messaging_client.send(successor.ip, successor.port, str(id))

    def receive_election_message(self, id: int):
        self.leader_elected = False

        if id == HALT:
            self.leader_elected = True
            if self.leader_node_id != self.node_id:
                self.send_election_message(HALT)
            return

        if id < self.node_id:
            return

        if id == self.node_id:
            self.leader_node_id = self.node_id
            self.leader_elected = True
            self.send_election_message(HALT)
            return

        self.leader_node_id = id
        self.send_election_message(id)
