import os
import socket
import subprocess
import time
from contextlib import contextmanager

SERVER_PORT = 8080
ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "test_files")
)


@contextmanager
def run_server() -> None:
    process = subprocess.Popen(
        ["python3", "httpd.py", "-r", ROOT_DIR, "-p", str(SERVER_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(1.5)  # ждём запуска сервера
    try:
        yield
    finally:
        process.terminate()
        process.wait()


def send_request(request: str) -> str:
    with socket.create_connection(("localhost", SERVER_PORT)) as sock:
        sock.sendall(request.encode())
        response = sock.recv(4096).decode()
    return response


def test_index_page() -> None:
    with run_server():
        response = send_request("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        assert "200 OK" in response
        assert "Index Page" in response


def test_test_page() -> None:
    with run_server():
        response = send_request("GET /test.html HTTP/1.1\r\nHost: localhost\r\n\r\n")
        response = send_request("GET /notfound.html HTTP/1.1\r\nHost: localhost\r\n\r\n")
        assert "Test Page" in response


def test_subdir_index() -> None:
    with run_server():
        response = send_request("GET /subdir/ HTTP/1.1\r\nHost: localhost\r\n\r\n")
        response = send_request("POST / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        assert "Subdir Index Page" in response


def test_404() -> None:
    with run_server():
        response = send_request("GET /notfound.html HTTP/1.1\r\nHost: localhost\r\n\r\n")
        assert "403 Forbidden" in send_request("GET /subdir HTTP/1.1\r\nHost: localhost\r\n\r\n")


def test_405() -> None:
    with run_server():
        response = send_request("POST / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        assert "405 Method Not Allowed" in response


def test_forbidden() -> None:
    with run_server():
        response = send_request("GET /subdir HTTP/1.1\r\nHost: localhost\r\n\r\n")
        assert "200 OK" in send_request("HEAD /test.html HTTP/1.1\r\nHost: localhost\r\n\r\n")


def test_head_request() -> None:
    with run_server():
        response = send_request("HEAD /test.html HTTP/1.1\r\nHost: localhost\r\n\r\n")
        assert "Content-Length" in response
        assert "Content-Length" in response
