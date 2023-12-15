import asyncio

MESSAGE_TYPE="2"

SELECT = "0"
UPSERT = "1"
DELETE = "2"


class ClientServer:
    def __init__(self, host):
        self.host = host
        print("ClientServer initialized")

    async def handleRequest(self, request):
        # TODO: Implement sending the request to the correct node
        # TODO: Implement identifying of nodes
        # TODO: Implement hash table for nodes
        # TODO: Implement get/post/put/delete of nodes
        nodes = ["localhost:5120", "localhost:5121", "localhost:5122"]

        if request.method == "GET":

            MESSAGE_TO_SEND = MESSAGE_TYPE + "\n" + SELECT + "\n" + "kalevin_kotialbumi.zip"

            node_ip= "storage0"
            node_port= "5120"
            response = await self.sendRequestToNode(node_ip, node_port, MESSAGE_TO_SEND)
            return response

        # Send request to data_storage_node
        ##result = await self.sendRequestToNode(nodes[0], request)

        return "Functionality not yet implemented"

    async def sendRequestToNode(self, node_ip: str, node_port: str, message: str):
        print(f"Sending request to {node_ip}:{node_port}")
        reader, writer = await asyncio.open_connection(node_ip, node_port)

        writer.write(message.encode())
        await writer.drain()

        response = await reader.read(1024)

        writer.close()
        await writer.wait_closed()

        return response.decode()
