MESSAGE_TYPE = "5"

class Node:
    id: int
    ip: str
    port: str
    successor_ip: str
    successor_port: str
    leader: bool

    def __init__(self, ip: str, port: int):
        self.id = nodes.__len__()
        self.ip = ip
        self.port = port
        self.successor_ip = ""
        self.successor_port = ""
        self.leader = False

    
nodes = []

def set_leader(node_id: int):
    for node in nodes:
        node.leader = node.id == node_id

def get_leader():
    for node in nodes:
        if node.leader:
            return node
    return None

def getNodes():
    return nodes

def add_node(ip: str, port: int):
    for node in nodes:
        if node.ip == ip and node.port == port:
            return node 

    new_node = Node(ip, port)
    nodes.append(new_node)
    update_successors(nodes)
    return new_node


def remove_node(ip: str, port: int):
    for node in nodes:
        if node.ip == ip and node.port == port:
            nodes.remove(node)
            update_successors(nodes)
            break

def update_successors(nodes):
    if len(nodes) == 0:
        return
    
    if len(nodes) == 1:
        nodes[0].successor_ip = nodes[0].ip
        nodes[0].successor_port = nodes[0].port
        return

    for i in range(len(nodes)):
        nodes[i].successor_ip = nodes[(i + 1) % len(nodes)].ip
        nodes[i].successor_port = nodes[(i + 1) % len(nodes)].port


