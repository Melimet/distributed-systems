from messaging_server import MessagingServer

HOST = "localhost"
PORT = 5120


def main():
    server = MessagingServer(HOST, PORT)
    server.start()


if __name__ == "__main__":
    main()
