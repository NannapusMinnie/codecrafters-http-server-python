import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_connection, client_address = server_socket.accept()

    request_data = client_connection.recv(1024).decode()
    all_lines = request_data.split("\r\n")
    first_line = all_lines[0] 
    request_line_components = first_line.split(" ")

    url_path = request_line_components[1]


    if url_path == "/":
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        
    client_connection.sendall(response)
    client_connection.close()

if __name__ == "__main__":
    main()
