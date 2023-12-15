import asyncio
from message_schemas import Message


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
