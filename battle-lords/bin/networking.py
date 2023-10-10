import socket


class NetworkAgent:
    def __init__(self, host: str = "localhost", port: int = 8421):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, msg_type: int, msg_body: str) -> list:
        try:
            self.client.send(str.encode(f"{self.id}|{msg_type}|{msg_body}"))
            reply = self.client.recv(2048).decode()
            return [0, reply.split("|")]

        except socket.error as e:
            return [1, str(e)]
