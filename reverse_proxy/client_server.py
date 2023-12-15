import asyncio

class ClientServer:
    MESSAGE_TYPE = "2"
    SELECT = "0"
    UPSERT = "1"
    DELETE = "2"

    def __init__(self, host):
        self.host = host
        self.nodes = [
            {"ip": "storage0", "port": "5120"},
            {"ip": "storage1", "port": "5121"},
            {"ip": "storage2", "port": "5122"}
        ]
        print("ClientServer initialized")

    async def handle_request(self, request):
        file_name = request.path_params["path"]
        node = self.nodes[2]

        if request.method == "GET":
            message = self.format_message(self.SELECT, file_name, "asd")
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
        print(f"Sending request to {node['ip']}:{node['port']}")
        reader, writer = await asyncio.open_connection(node['ip'], node['port'])

        writer.write(message.encode())
        await writer.drain()

        response = await reader.read(1024)

        writer.close()
        await writer.wait_closed()

        return response.decode()

    def format_message(self, operation, file_name, data):
        return f"{self.MESSAGE_TYPE}\n{operation}\n{file_name}\n{data}"