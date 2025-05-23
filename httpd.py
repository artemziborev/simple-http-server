import os
import argparse
from dotenv import load_dotenv
from core.server import start_server


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Simple HTTP Server")

    parser.add_argument(
        "-r", "--root",
        default=os.getenv("DOCUMENT_ROOT"),
        required=not os.getenv("DOCUMENT_ROOT"),
        help="Root directory for serving files"
    )
    parser.add_argument(
        "--host",
        default=os.getenv("SERVER_HOST", "0.0.0.0"),
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=int(os.getenv("SERVER_PORT", "8080")),
        help="Port to listen on (default: 8080)"
    )
    parser.add_argument(
        "-b", "--backlog",
        type=int,
        default=int(os.getenv("SERVER_BACKLOG", "1024")),
        help="Maximum number of pending connections"
    )
    parser.add_argument(
        "--buffer-size",
        type=int,
        default=int(os.getenv("SERVER_BUFFER_SIZE", "4096")),
        help="Buffer size for reading data"
    )

    args = parser.parse_args()

    start_server(
        root_directory=args.root,
        host=args.host,
        port=args.port,
        backlog=args.backlog,
        buffer_size=args.buffer_size
    )


if __name__ == "__main__":
    main()
