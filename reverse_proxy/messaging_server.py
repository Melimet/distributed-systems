import asyncio
from message_schemas import Message, MessageType, NodeRegistryMessage

class MessagingServer:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.ip, self.port) 
        
        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        data = await reader.read(1024)
        message = data.decode()

        sender_ip = writer.get_extra_info('peername')[0]
        sender_port = writer.get_extra_info('peername')[1]

        response_message = await self.handle_request(message, sender_ip, sender_port)
        writer.write(response_message.data.encode())
        await writer.drain()
        writer.close()

    
    async def handle_request(self, data: str, sender_ip: str, sender_port: str) -> Message:
        message = Message(data)

        if(message.get_type() == MessageType.NODE_REGISTRY):
            NodeRegistryMessage.register(message, sender_ip, sender_port)