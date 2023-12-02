import socket  
  
def main():  
    host = 'localhost' 

    port = 5123 
  
    data_storage_node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    # data_storage_node_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    data_storage_node_socket.bind((host, port))  
  
    data_storage_node_socket.listen(1)  
    print('Data storage node is listening on port 5000')  
  
    conn, address = data_storage_node_socket.accept()  
    print("Connection from: " + str(address))  
  
    while True:  
        data = conn.recv(1024).decode()  
        if not data:  
            break  
        print("Received data from reverse proxy: " + str(data))  
  
        data = input(' -> ')  
        conn.send(data.encode())  
  
    conn.close()  
  
if __name__ == '__main__':  
    main()