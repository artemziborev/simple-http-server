import os
import socket
import urllib.parse

from core.headers import build_headers
from utils.mime import guess_mime_type


class Connection:
    def __init__(
        self,
        client_socket: socket.socket,
        root_directory: str,
        buffer_size: int
    ) -> None:
        self.socket = client_socket
        self.root = root_directory
        self.buffer_size = buffer_size
        self.recv_buffer = b""
        self.keep_alive = False

    def handle_read(self) -> bool:
        try:
            data = self.socket.recv(self.buffer_size)
            if not data:
                return False

            self.recv_buffer += data
            if b"\r\n\r\n" not in self.recv_buffer:
                return True

            request = self.recv_buffer.decode("utf-8", errors="replace")
            return self._handle_request(request)
        except (ConnectionResetError, socket.error):
            return False

    def _handle_request(self, request: str) -> bool:
        lines = request.split("\r\n")
        request_line = lines[0]
        parts = request_line.split()

        if len(parts) < 3:
            self._send_response(400, b"Bad Request")
            return False

        method, path, _ = parts
        decoded_path = urllib.parse.unquote(path.split("?", 1)[0])
        full_path = os.path.join(self.root, decoded_path.lstrip("/"))

        if not os.path.abspath(full_path).startswith(os.path.abspath(self.root)):
            self._send_response(403, b"Forbidden")
            return False

        if os.path.isdir(full_path):
            full_path = os.path.join(full_path, "index.html")

        if not os.path.exists(full_path):
            self._send_response(404, b"Not Found")
            return False

        if method not in ("GET", "HEAD"):
            self._send_response(405, b"Method Not Allowed")
            return False

        try:
            with open(full_path, "rb") as f:
                content = f.read() if method == "GET" else b""
                content_type = guess_mime_type(full_path)
                headers = build_headers(
                    status_code=200,
                    content_length=len(content),
                    content_type=content_type
                )
                self.socket.sendall(headers + content)
        except PermissionError:
            self._send_response(403, b"Forbidden")
            return False

        return False

    def _send_response(self, status_code: int, body: bytes) -> None:
        headers = build_headers(
            status_code=status_code,
            content_length=len(body),
            content_type="text/plain"
        )
        self.socket.sendall(headers + body)

    def close(self) -> None:
        try:
            self.socket.close()
        except OSError:
            pass
