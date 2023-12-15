MESSAGE_TYPE = "5"

class Node:
    id: int
    ip: str
    port: str
    successor_ip: str
    successor_port: str

    def __init__(self, ip: str, port: int):
        self.id = nodes.__len__()
        self.ip = ip
        self.port = port
        self.successor_ip = ""
        self.successor_port = ""

nodes = []

def getNodes():
    return nodes

def add_node(ip: str, port: int):
    if not any(node.ip == ip and node.port == port for node in nodes):
        nodes.append(Node(ip, port))
        update_successors(nodes)

def remove_node(ip: str, port: int):
    for node in nodes:
        if node.ip == ip and node.port == port:
            nodes.remove(node)
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

