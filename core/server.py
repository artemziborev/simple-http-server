import socket
import select
from typing import Dict

from core.connection import Connection


def start_server(
    root_directory: str,
    host: str,
    port: int,
    backlog: int,
    buffer_size: int
) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)
    server_socket.bind((host, port))
    server_socket.listen(backlog)

    print(
        f"Server running on {host}:{port}, "
        f"serving files from {root_directory}"
    )

    epoll = select.epoll()
    epoll.register(server_socket.fileno(), select.EPOLLIN)

    connections: Dict[int, Connection] = {}

    try:
        while True:
            events = epoll.poll(1)
            for fileno, event in events:
                if fileno == server_socket.fileno():
                    client_socket, client_addr = server_socket.accept()
                    client_socket.setblocking(False)
                    epoll.register(client_socket.fileno(), select.EPOLLIN)
                    connections[client_socket.fileno()] = Connection(
                        client_socket=client_socket,
                        root_directory=root_directory,
                        buffer_size=buffer_size
                    )
                    print(f"Accepted connection from {client_addr}")
                elif event & select.EPOLLIN:
                    conn = connections.get(fileno)
                    if conn and not conn.handle_read():
                        epoll.unregister(fileno)
                        conn.close()
                        del connections[fileno]
                elif event & (select.EPOLLHUP | select.EPOLLERR):
                    conn = connections.get(fileno)
                    if conn:
                        epoll.unregister(fileno)
                        conn.close()
                        del connections[fileno]
    finally:
        epoll.unregister(server_socket.fileno())
        epoll.close()
        server_socket.close()
