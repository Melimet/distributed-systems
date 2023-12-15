from enum import Enum
from typing import Optional

from reverse_proxy.node_registry import Node, NodeRegistry

class MessageType(Enum):
    ERROR = -1
    ACK = 0
    ELECTION = 1
    FILE = 2
    SYNC = 3
    HEARTBEAT = 4
    NODE_REGISTRY = 5


class Message:
    """
    Base class for all messages. Format for data string is as follows:

    ```
    <MESSAGE_TYPE>
    <ARBITRARY_DATA>
    ```

    where
        MESSAGE_TYPE   = integer representing the type of message (eg. 0 for election)
        ARBITRARY_DATA = a multi-line string representing the arbitrary data of the message
    """

    data: str

    def __init__(self, data: str = ""):
        self.data = data

    def get_type(self) -> MessageType:
        return MessageType(int(self.get_line(0)))

    def is_ok(self) -> bool:
        return self.get_type() != MessageType.ERROR

    def get_lines(self) -> list:
        return self.data.strip().split("\n")

    def get_line(self, index: int) -> Optional[str]:
        lines = self.get_lines()
        if index >= len(lines):
            return None
        return lines[index]


class NodeRegistryMessage(Message):
    """
    Message used for registering a node to the reverse proxy.

    ```
    5
    <NODE_ID>
    <SUCCESSOR_IP>
    <SUCCESSOR_PORT>
    ```

    where
        NODE_ID         = id of the node that reverse proxy assigned to it (empty if registering)
        SUCCESSOR_IP    = ip of the successor node that is needed for  (empty if registering)
        SUCCESSOR_PORT  = port of the successor node that is needed for  (empty if registering)
    """

    def register(data: str, sender_ip: str, sender_port: str) -> "NodeRegistryMessage":
        new_node = Node(sender_ip, sender_port)
        NodeRegistry.add_node(new_node)
        
        data = f"""
        {MessageType.NODE_REGISTRY.value}
        {new_node.id}
        {new_node.successor_ip}
        {new_node.successor_port}
        """

        return NodeRegistryMessage(data)