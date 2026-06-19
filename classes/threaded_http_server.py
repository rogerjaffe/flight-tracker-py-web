import os
import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer


class ThreadedHTTPServer:
  def __init__(self, directory_to_serve):
    self.directory = str(os.path.abspath(directory_to_serve))

    # Use a lambda to pass the directory configuration cleanly
    handler_factory = lambda *args, **kwargs: SimpleHTTPRequestHandler(
      *args, directory=self.directory, **kwargs
    )

    self.server = TCPServer(("127.0.0.1", 0), handler_factory)
    self.port = self.server.socket.getsockname()[1]  # Extract the actual port integer

    self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
    self.thread.start()
