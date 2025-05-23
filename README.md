
# Simple HTTP Server

This is a simple HTTP server implemented in Python with `asyncio`. It supports basic HTTP functionality, including GET and HEAD methods, directory indexing, and MIME type detection.

## Features
- Asynchronous, non-blocking I/O with `asyncio`
- Support for multiple worker processes
- Directory indexing (`index.html` support)
- Basic MIME type detection
- Proper handling of HTTP methods:
  - **200 OK** for successful requests
  - **403 Forbidden** for directory access without `index.html`
  - **404 Not Found** for missing files
  - **405 Method Not Allowed** for unsupported methods

## Getting Started

### Requirements
- Python 3.12 or higher

### Installation
Clone the repository or download the source code:

```bash
git clone https://github.com/..../simple-http-server.git
cd simple-http-server
```

### Running the Server

```bash
python3 httpd.py -r /path/to/document_root -w 4
```

**Arguments:**

- **-r, --root**: Path to the document root (required)
- **-w, --workers**: Number of worker processes (default: 1)

**Example:**

```bash
python3 httpd.py -r ./www -w 4
```

### Testing the Server
To test the server, you can use **curl** or a web browser:

```bash
curl http://localhost:8080/
curl http://localhost:8080/index.html
curl http://localhost:8080/images/logo.png
```

### Supported MIME Types
The server supports the following MIME types:

- `.html` — text/html
- `.css` — text/css
- `.js` — application/javascript
- `.jpg` / `.jpeg` — image/jpeg
- `.png` — image/png
- `.gif` — image/gif
- `.swf` — application/x-shockwave-flash
- `.txt` — text/plain

### Known Issues
- Directory access without `index.html` returns **403 Forbidden**.
- No support for HTTP/2.
- No SSL/TLS support.
- Basic error handling.

### To Do
- Add support for URL-encoded filenames.
- Improve MIME type detection.
- Optimize worker management.
- Add logging and monitoring.

### License
MIT License. Feel free to use, modify, and distribute.

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Author
Developed by Artem Ziborev
