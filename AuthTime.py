from time import sleep
from os import remove
import threading

ThreadStore = []
Lock = threading.Lock()


class Auth(threading.Thread):
    def __init__(self, UserID, Login):
        threading.Thread.__init__(self)
        self.ID = UserID
        self.name = Login
        self.fileName = self.name + ".txt"

    def CreateFile(self, Password):
        File = open(self.fileName, 'w')
        File.write(str(self.ID))
        File.write(self.name)
        File.write(Password)
        File.close()

    def run(self):
        Lock.acquire()
        sleep(1)
        print(self.name, " started!")
        Lock.release()
        sleep(40)
        remove(self.fileName)
        # DatabaseQuery.DataBaseOperate.DisableResetFlag(DatabaseQuery.DataBaseOperate(), self.UserLogin)
        Lock.acquire()
        sleep(1)
        print(self.name, " down!")
        Lock.release()


class Manager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        Lock.acquire()
        print("Manager created!")
        Lock.release()

    def run(self):
        Lock.acquire()
        print("Manager started!")
        sleep(2)
        Lock.release()
        while True:
            print(ThreadStore)
            for T in ThreadStore:
                if not T.is_alive():
                    ThreadStore.remove(T)
            sleep(10)
