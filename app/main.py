import socket  # noqa: F401
import threading
import sys
import os

def handle_client(client_connection, directory_path):
    try:
        request_data = client_connection.recv(1024).decode()
        if not request_data:
            return
         
        all_lines = request_data.split("\r\n")
        first_line = all_lines[0] 
        request_line_components = first_line.split(" ")
        
        url_path = request_line_components[1]
        http_method = request_line_components[0]
        
        
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

        elif url_path.startswith("/files/"):
            filename = url_path[7:]
            file_path = os.path.join(directory_path, filename)

            if http_method == "GET":
                if os.path.exists(file_path):
                    with open(file_path, "r") as file:
                        file_content = file.read()           
                    content_length = len(file_content)
                    response_text = (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: application/octet-stream\r\n"
                        f"Content-Length: {content_length}\r\n"
                        f"\r\n"
                        f"{file_content}"
                    )
                    response = response_text.encode()
                else:
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"

            elif http_method == "POST":
                request_parts_by_body = request_data.split("\r\n\r\n", 1)
                request_body = request_parts_by_body[1]

                with open(file_path, "w") as file:
                    file.write(request_body)  
                response = b"HTTP/1.1 201 Created\r\n\r\n"
            else:
                response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        
        client_connection.sendall(response)
    finally:
        client_connection.close()
        

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    directory_path = ""
    if "--directory" in sys.argv:
        dir_index = sys.argv.index("--directory")
        directory_path = sys.argv[dir_index + 1]

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=[client_connection, directory_path])
        client_thread.start()

if __name__ == "__main__":
    main()
