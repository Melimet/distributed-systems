import asyncio
from messaging_server import MessagingServer
from config import port, ip

IP = ip
PORT = port


async def main():
    server = MessagingServer(IP, PORT)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
