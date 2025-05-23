from datetime import datetime
from typing import Dict


STATUS_MESSAGES: Dict[int, str] = {
    200: "OK",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
}


def build_headers(
    status_code: int,
    content_length: int,
    content_type: str
) -> bytes:
    reason = STATUS_MESSAGES.get(status_code, "Unknown")
    date_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    headers = [
        f"HTTP/1.1 {status_code} {reason}",
        f"Date: {date_str}",
        "Server: SimpleHTTPServer",
        f"Content-Length: {content_length}",
        f"Content-Type: {content_type}",
        "Connection: close",
        "",
        ""
    ]

    return "\r\n".join(headers).encode("utf-8")
