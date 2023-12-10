from messaging import MessagingServer, MessagingClient

HOST = "localhost"
PORT = 5123


def main():
    server = MessagingServer(HOST, PORT)
    server.start()

    while True:
        input("Press any key to exit\n")
        break


if __name__ == "__main__":
    main()
