import asyncio
from messaging_server import MessagingServer
from config import port

HOST = "localhost"
PORT = port


async def main():
    server = MessagingServer(HOST, PORT)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
