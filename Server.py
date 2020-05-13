import socket
import json
import selectors
import sys
import Validation
import DatabaseQuery


class Server:
    def __init__(self):
        self.Selector = selectors.DefaultSelector()
        self.Socket = socket.socket()
        self.Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.Address = None
        self.Port = None
        self.DatabaseOperation = None

    # Setting server to listen incoming connections
    def SetServer(self):
        self.DatabaseOperation = DatabaseQuery.DataBaseOperate()
        self.Socket.bind((self.Address, self.Port))
        self.Socket.listen(100)
        self.Socket.setblocking(False)
        print("Server's working on ", self.Address)
        self.Selector.register(self.Socket, selectors.EVENT_READ, self.AcceptConnection)

    # Accepting connection
    def AcceptConnection(self, socket, mask):
        Connection, Address = socket.accept()
        print("Accepted  from ", Address)
        Connection.setblocking(False)
        self.Selector.register(Connection, selectors.EVENT_READ, self.ProcessEvent)

    # Serving connection
    def ProcessEvent(self, Conn, mask):
        self.Received = self.Read(Conn)

        if self.Received is not None:
            Data = self.Write(self.Received)
            self.Send(Data, Conn)
        else:
            Data = self.Write([10])
            self.Send(Data, Conn)
        print("Data: ", Data)
        self.CloseConnection(Conn)

    # Checking and decoding JSON data
    def Read(self, Conn):
        DataRec = self.Receieve(Conn)
        if self.isJSON(DataRec):
            Data = json.loads(DataRec.decode())
            print("Data received: ", Data)
            return self.ManageOperations(Data)
        else:
            return None

    # Sending JSON data
    def Send(self, Data, Conn):
        Conn.send(Data)

    # Creating JSON (encoding)
    def Write(self, Data):
        DataToSend = (json.dumps(Data)).encode()
        return DataToSend

    # Receive data
    def Receieve(self, Conn):
        DataRec = Conn.recv(4096).strip()
        return DataRec

    # Checking if client send data as JSON
    def isJSON(self, Data):
        try:
            json.loads(Data)
        except ValueError as e:
            return False
        return True

    # Closing connection
    def CloseConnection(self, Conn):
        print("Closing ", Conn)
        self.Selector.unregister(Conn)
        Conn.close()

    # Server main loop
    def ServerLoop(self):
        while True:
            Events = self.Selector.select(timeout=None)
            for key, mask in Events:
                CallBack = key.data
                CallBack(key.fileobj, mask)

    # Choosing client action
    def ManageOperations(self, DictArg):
        Operation = DictArg['Action']
        if Operation == 'CreateUser':
            return self.DatabaseOperation.CreateUser(DictArg)
        elif Operation == 'Login':
            return self.DatabaseOperation.Login(DictArg)
        elif Operation == 'ShowUsers':
            return self.DatabaseOperation.ShowUsers(DictArg)
        elif Operation == 'CreateGroup':
            return self.DatabaseOperation.CreateGroup(DictArg)
        elif Operation == 'DeleteGroup':
            return self.DatabaseOperation.DeleteGroup(DictArg)
        elif Operation == 'AddToGroup':
            return self.DatabaseOperation.AddToGroup(DictArg)
        elif Operation == 'ShowGroups':
            return self.DatabaseOperation.ShowGroups(DictArg)
        elif Operation == 'ShowUsers':
            return self.DatabaseOperation.ShowUsers(DictArg)
        elif Operation == 'CreateTask':
            return self.DatabaseOperation.CreateTask(DictArg)
        elif Operation == 'ShowTask':
            return self.DatabaseOperation.ShowTask(DictArg)
        elif Operation == 'CreateSubTask':
            return self.DatabaseOperation.CreateSubTask(DictArg)
        elif Operation == 'ShowSubTask':
            return self.DatabaseOperation.ShowSubTask(DictArg)
        elif Operation == 'ChangePassword':
            return self.DatabaseOperation.ChangePassword(DictArg)
        elif Operation == 'ChangeTaskStatus':
            return self.DatabaseOperation.ChangeTaskStatus(DictArg)
        elif Operation == 'LeaderView':
            return self.DatabaseOperation.LeaderView(DictArg)
        elif Operation == 'ResetPassword':
            return self.DatabaseOperation.ResetPassword(DictArg)
        else:
            return [300]


if __name__ == '__main__':
    ServerProcess = Server()
    validator = Validation.Validate(sys.argv, ServerProcess, "Server")
    validation_code = validator.validate()

    if validation_code == 0:
        ServerProcess.SetServer()
        ServerProcess.ServerLoop()
