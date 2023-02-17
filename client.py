import socket
import pickle

class Client:
    """
    Use to establish connection with Server (socket)
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.headersize = 10

    def connect(self):
        self.socket.connect((self.host, self.port))

    def receive_data(self):
        fullPayload = b""
        newPayload = True
        
        while True:
            payload = self.socket.recv(16)
            if newPayload:
                # print(f"New Message Length: {payload[:self.headersize]}")
                payloadLength = int(payload[:self.headersize])
                newPayload = False

            fullPayload += payload
            
            if len(fullPayload) - self.headersize == payloadLength:
                # newPayload = True
                # fullPayload = b""
                return pickle.loads(fullPayload[self.headersize:])

    def send_data(self, payload):
        payload = pickle.dumps(payload)
        payload = bytes(f"{len(payload):<{self.headersize}}", "utf-8") + payload
        self.socket.send(payload)
        
    def close(self):
        print("Closing client socket.")
        self.socket.close()
