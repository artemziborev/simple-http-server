import os
from utils.mime_types import get_mime_type
from core.headers import HeadersBuilder


class FileHandler:
    def __init__(self, root_directory):
        self.root_directory = os.path.abspath(root_directory)

    def handle(self, client_socket):
        try:
            # Read the client request
            request = client_socket.recv(4096).decode()
            if not request:
                return

            # Parse the request line (e.g., "GET /index.html HTTP/1.1")
            request_line = request.splitlines()[0]
            method, path, _ = request_line.split()

            # Only support GET and HEAD methods
            if method not in ["GET", "HEAD"]:
                self._send_response(client_socket, "405 Method Not Allowed", b"")
                return

            # Resolve the requested file path
            file_path = os.path.normpath(os.path.join(self.root_directory, path.lstrip("/")))

            # If the path is a directory, look for index.html
            if os.path.isdir(file_path):
                index_file = os.path.join(file_path, "index.html")
                if os.path.isfile(index_file):
                    file_path = index_file
                else:
                    self._send_response(client_socket, "403 Forbidden", b"")
                    return

            # Check if the requested file exists
            if not os.path.isfile(file_path):
                self._send_response(client_socket, "404 Not Found", b"")
                return

            # Read the file content
            with open(file_path, "rb") as file:
                content = file.read()

            # Build and send headers
            headers = HeadersBuilder(file_path, content).build()
            client_socket.send(headers.encode())

            # Send the file content for GET requests
            if method == "GET":
                client_socket.send(content)

        except Exception as e:
            print(f"Error in FileHandler: {e}")

    def _send_response(self, client_socket, status, body):
        headers = f"HTTP/1.1 {status}\r\nConnection: close\r\n\r\n"
        client_socket.send(headers.encode())
        if body:
            client_socket.send(body)
