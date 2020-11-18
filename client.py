import time
import socket


class ClientError(Exception):
    """Client exception class"""
    pass


class Client:

    def __init__(self, host, port, timeout=None):

        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((self.host, self.port), self.timeout)
        self.data = self.get()
 
    def get(self):
        self.key = 'stars'
        self.sock.sendall(self.key.encode("utf8"))

        try:
            data = self.sock.recv(1024)
            info = data.decode()
            if not data:
                raise ClientError 
            return int(info)           
        except ValueError:
            raise ClientError
        except socket.timeout:
            print("send data timeout")
        except socket.error as err:
            print("send data error:", err)
     

    def exit(self):
        try:
            self.sock.close()
        except socket.error as err:
            raise ClientError("Error. Do not close the connection", err)
        


