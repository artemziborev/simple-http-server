import mimetypes


def guess_mime_type(path: str) -> str:
    mime_type, _ = mimetypes.guess_type(path)

    if mime_type is None:
        return "application/octet-stream"

    return mime_type
