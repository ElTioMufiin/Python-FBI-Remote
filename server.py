import os
import socket
import struct
import sys
import threading
import time
import urllib

try:
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer
    from urllib import quote

except ImportError:
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer
    from urllib.parse import quote    

class MyServer(TCPServer):
    def server_bind(self):
        import socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

print('Opening HTTP server on port ' + str(hostPort))
server = MyServer(('', hostPort), SimpleHTTPRequestHandler)
thread = threading.Thread(target=server.serve_forever)
thread.start()

try:
    print('Sending URL(s) to ' + target_ip + ' on port 5000...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, 5000))
    sock.sendall(struct.pack('!L', len(file_list_payloadBytes)) + file_list_payloadBytes)
    while len(sock.recv(1)) < 1:
        time.sleep(0.05)
    sock.close()

finally:
    print('Shutting down HTTP server...')
    server.shutdown()