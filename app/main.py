import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_connection, client_address = server_socket.accept()
    response = b"HTTP/1.1 200 OK\r\n\r\n"
    client_connection.sendall(response)
    client_connection.close()

if __name__ == "__main__":
    main()
