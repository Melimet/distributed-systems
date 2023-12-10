from typing import List, Tuple, Optional

HALT = -1


def get_nodes():
    """
    TODO: Remove this and replace it with a RPC call to node registry.

    Returns:
        id: id of the node
        node_list: list of tuples containing id and ip of all nodes
    """

    id = 0
    node_list = [(0, "ip_0"), (1, "ip_1"), (2, "ip_2")]

    return id, node_list


class Node:
    id: int
    node_list: List[Tuple[int, str]]
    leader: Optional[int]
    leader_elected: bool

    def __init__(self):
        id, node_list = get_nodes()
        self.id = id
        self.node_list = node_list
        self.leader = None
        self.leader_elected = False

    def get_successor(self):
        successor_index = (self.id + 1) % len(self.node_list)
        return self.node_list[successor_index]

    def start_leader_election(self):
        """
        Leader is elected with LCR algorithm. Any node can initiate the election.
        The node with the highest id will be elected as the leader.
        """
        self.send_election_message(self.id)

    def send_election_message(self, id: int):
        # TODO: send message to successor
        #       should retry if successor does not respond
        #       should get new successor if current successor fails
        successor_ip = self.get_successor()[1]

    def is_leader(self):
        return self.leader == self.id

    def receive_election_message(self, id: int):
        self.leader_elected = False

        if id == HALT:
            self.leader_elected = True
            if not self.is_leader():
                self.send_election_message(HALT)
            return

        if id < self.id:
            return

        if id == self.id:
            self.leader = self.id
            self.leader_elected = True
            self.send_election_message(HALT)
            return

        self.leader = id
        self.send_election_message(id)
