import socket
import pickle


class Server:
    """
    UUse to establish a Server (with socket)
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket()

        self.__data = []
        self.conn, self.address = None, None
        self.headersize = 10

    def start(self):
        print(f"Creating server at {self.host}:{self.port}")
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        self.conn, self.address = self.socket.accept()
        # print(f"Connection from {self.address}")

    def send_data(self, payload):
        payload = pickle.dumps(payload)
        payload = bytes(f"{len(payload):<{self.headersize}}", "utf-8") + payload
        self.conn.send(payload)

    def receive_data(self):
        fullPayload = b""
        newPayload = True
        
        while True:
            payload = self.conn.recv(16)
            if newPayload:
                # print(f"New Message Length: {payload[:self.headersize]}")
                payloadLength = int(payload[:self.headersize])
                newPayload = False

            fullPayload += payload
            
            if len(fullPayload) - self.headersize == payloadLength:
                # newPayload = True
                # fullPayload = b""
                return pickle.loads(fullPayload[self.headersize:])
        
        # This may allow arbitrary code execution. Only connect to trusted connections!!!
        # return pickle.loads(b''.join(self.__data))


    def close(self):
        print("Closing server socket.")
        self.socket.close()
