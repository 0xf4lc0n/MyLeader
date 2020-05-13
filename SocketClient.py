import socket
import json


class Client:
    def __init__(self):
        self.Socket = None
        self.Address = None
        self.Port = None

    # Managing connection

    def SetConnection(self):
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.Socket.connect((self.Address, self.Port))
            return True
        except socket.error as e:
            print(e.strerror)
            return False

    def CloseConnection(self):
        self.Socket.shutdown(2)
        self.Socket.close()

    # Sending/Receiving data

    def Send(self, RawData):
        Data = self.Pack(RawData)
        self.Socket.send(Data)

    def Receive(self):
        DataRec = self.Socket.recv(4096).strip()
        Received = self.Unpack(DataRec)
        return Received

    # Packing/Unpacking data

    def Pack(self, Data):
        DataToSend = (json.dumps(Data)).encode()
        return DataToSend

    def Unpack(self, Data):
        Received = json.loads(Data.decode())
        return Received

    # Client process

    def ProcessEvent(self, RawData):
        if self.SetConnection():
            self.Send(RawData)
            Recieved = self.Receive()
            self.CloseConnection()
            return Recieved
        else:
            return 10
