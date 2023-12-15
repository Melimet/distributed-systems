import asyncio
from message_schemas import Message

REVERSE_PROXY_IP = "proxy"
REVERSE_PROXY_PORT = 5119


class MessagingClient:
    def __init__(self):
        pass

    async def send(self, ip: str, port: int, message: str) -> Message:
        reader, writer = await asyncio.open_connection(ip, port)

        writer.write(message.encode())
        await writer.drain()

        response_data = await reader.read(1024)

        writer.close()
        await writer.wait_closed()

        return Message(response_data.decode())

    async def send_to_reverse_proxy(self, message: str) -> Message:
        return await self.send(REVERSE_PROXY_IP, REVERSE_PROXY_PORT, message)
