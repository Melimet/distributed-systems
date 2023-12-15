import socket  
  
def main():  
    host = '0.0.0.0'
    port = 5124
  
    reverse_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    reverse_proxy_socket.bind((host, port))  
    reverse_proxy_socket.listen(1)  
  
    print('Reverse proxy is listening on port 6000')  
  
    while True:  
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        client_socket.connect((host, 5123))  
  
        message = input(" -> ")  
        while message.lower().strip() != 'bye':  
            client_socket.send(message.encode())  
            data = client_socket.recv(1024).decode()  
  
            print('Received from data storage node: ' + data)  
  
            message = input(" -> ")  
  
        client_socket.close()  
  
if __name__ == '__main__':  
    main()  