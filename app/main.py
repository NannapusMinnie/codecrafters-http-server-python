import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_connection, client_address = server_socket.accept()

    request_data = client_connection.recv(1024).decode()
    all_lines = request_data.split("\r\n")
    first_line = all_lines[0] 
    request_line_components = first_line.split(" ")

    url_path = request_line_components[1]


    if url_path == "/":
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    elif url_path.startswith("/echo/"):
        echo_string = url_path[6:]
        content_length = len(echo_string)
        response_text = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {content_length}\r\n"
            f"\r\n"
            f"{echo_string}"
        )
        response = response_text.encode()
    elif url_path == "/user-agent":
        user_agent_value = ""
        for line in all_lines[1:]:
            if line.lower().startswith("user-agent:"):
                user_agent_value = line.split(": ", 1)[1]
                break 
        content_length = len(user_agent_value)
        response_text = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {content_length}\r\n"
            f"\r\n"
            f"{user_agent_value}"
        )
        response = response_text.encode()
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    client_connection.sendall(response)
    client_connection.close()

if __name__ == "__main__":
    main()
