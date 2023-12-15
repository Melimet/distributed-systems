import socket
from messaging_client import MessagingClient
from message_schemas import MessageType, FileOperation, Message, FileMessage


class MessagingClient:
    def __init__(self):
        pass

    def send(self, ip: str, port: int, message: str) -> Message:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((ip, port))
            client_socket.sendall(message.encode())

            print(f"Waiting response")

            response = client_socket.recv(1024).decode()
            return Message(response)


def test_me():
    """
    Node 3 is hard coded to have the highest id, so in testing it will always be the leader.
    """

    client = MessagingClient()
    node_1_port = 5120
    node_2_port = 5121
    node_3_port = 5122

    upsert_hello_world_message = FileMessage.from_operation(
        FileOperation.UPSERT,
        "hello.txt",
        "Hello World!",
    )

    select_hello_world_message = FileMessage.from_operation(
        FileOperation.SELECT,
        "hello.txt",
        "",
    )

    # UPSERT hello.txt "Hello World!" on node 3 (leader)
    response = client.send("0.0.0.0", node_3_port, upsert_hello_world_message.data)
    if response.is_ok():
        print("Got this ACK message from node 3:", response.data)
    else:
        print("Got this ERROR message from node 3:", response.data)
        return

    # SELECT hello.txt on node 1 (follower)
    response = client.send("0.0.0.0", node_1_port, select_hello_world_message.data)
    if response.is_ok():
        print("Got this SELECT from node 1:", response.data)
    else:
        print("Got this ERROR message from node 1:", response.data)
        return


if __name__ == "__main__":
    test_me()
