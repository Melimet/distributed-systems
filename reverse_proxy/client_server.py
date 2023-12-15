import asyncio

MESSAGE_TYPE="2"

SELECT = "0"
UPSERT = "1"
DELETE = "2"
FILE_NAME = "kalevin_kotialbumi.zip"


class ClientServer:
    def __init__(self, host):
        self.host = host
        print("ClientServer initialized")

    async def handleRequest(self, request):
        # TODO: Implement sending the request to the correct node
        # TODO: Implement identifying of nodes
        # TODO: Implement hash table for nodes
        # TODO: Implement post/put/delete of nodes
        nodes = [{
            "ip": "storage0",
            "port": "5120"
        },
            {
            "ip": "storage1",
            "port": "5121"
        },
            {
            "ip": "storage2",
            "port": "5122"
        }]

        if request.method == "GET":

            MESSAGE_TO_SEND = MESSAGE_TYPE + "\n" + SELECT + "\n" + FILE_NAME + "\n" + "asd"

            node_ip= "nodes[0].ip"
            node_port= "nodes[0].port"
            response = await self.sendRequestToNode(node_ip, node_port, MESSAGE_TO_SEND)
            return response


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
