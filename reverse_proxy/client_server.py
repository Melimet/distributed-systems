import asyncio

class ClientServer:
    """
    Represents a client-server communication handler.

    Attributes:
        MESSAGE_TYPE (str): The message type for communication.
        SELECT (str): The select operation code.
        UPSERT (str): The upsert operation code.
        DELETE (str): The delete operation code.
        host (str): The host address of the server.
        nodes (list): The list of nodes to communicate with.
    """

    MESSAGE_TYPE = "2"
    SELECT = "0"
    UPSERT = "1"
    DELETE = "2"

    def __init__(self, host):
        """
        Initializes a ClientServer instance.

        Args:
            host (str): The host address of the server.
        """
        self.host = host
        self.nodes = [
            {"ip": "storage0", "port": "5120"},
            {"ip": "storage1", "port": "5121"},
            {"ip": "storage2", "port": "5122"}
        ]
        print("ClientServer initialized")

    async def handle_request(self, request):
        """
        Handles a client request.

        Args:
            request: The client request object.

        Returns:
            The response from the server.
        """
        file_name = request.path_params["path"]
        node = self.nodes[2]

        if request.method == "GET":
            message = self.format_message(self.SELECT, file_name, "")
            return await self.send_request_to_node(node, message)

        elif request.method == "POST":
            data = await request.body()
            message = self.format_message(self.UPSERT, file_name, data.decode())
            return  await self.send_request_to_node(node, message)

        elif request.method == "DELETE":
            message = self.format_message(self.DELETE, file_name, "")
            return await self.send_request_to_node(node, message)

        return "Functionality not yet implemented"

    async def send_request_to_node(self, node, message):
        """
        Sends a request to a node.

        Args:
            node (dict): The node to send the request to.
            message (str): The message to send.

        Returns:
            The response from the node.
        """
        print(f"Sending request to {node['ip']}:{node['port']}")
        reader, writer = await asyncio.open_connection(node['ip'], node['port'])

        writer.write(message.encode())
        await writer.drain()

        response = await reader.read(1024)

        writer.close()
        await writer.wait_closed()

        return response.decode()

    def format_message(self, operation, file_name, data):
        """
        Formats a message for communication.

        Args:
            operation (str): The operation code.
            file_name (str): The file name.
            data (str): The data.

        Returns:
            The formatted message.
        """
        return f"{self.MESSAGE_TYPE}\n{operation}\n{file_name}\n{data}"