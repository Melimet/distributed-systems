import socket
from messaging import MessagingServer, MessagingClient

HOST = "localhost"
PORT = 5123


def main():
    client = MessagingClient()
    server = MessagingServer(HOST, PORT, client)
    server.start()


if __name__ == "__main__":
    main()
