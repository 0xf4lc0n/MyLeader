import hashlib
import os
import SocketClient
from prettytable import PrettyTable


class ClientQuery:
    def __init__(self):
        self.HashMethod = hashlib.sha256()

    def CreateUser(self):
        FirstName = input("First name: ")
        LastName = input("Last name: ")
        Email = input("Email: ")
        Login = input("Login: ")
        Password = input("Password: ")
        self.HashMethod = hashlib.sha256()
        self.HashMethod.update(Password.encode())
        Hash = (self.HashMethod.hexdigest()).upper()

        return {'Action': 'CreateUser', 'Args': {'Login': Login, 'Password': Hash, 'FirstName': FirstName, 'LastName':
            LastName, 'Email': Email}}

    def Login(self):
        Login = input("Login: ")
        Password = input("Password: ")
        self.HashMethod = hashlib.sha256()
        self.HashMethod.update(Password.encode())
        Hash = (self.HashMethod.hexdigest()).upper()

        return {'Action': 'Login', 'Args': {'Login': Login, 'Password': Hash}}

    def ChangePassword(self):
        Login = input("Login: ")
        OldPassword = input("Old password: ")
        NewPassword = input("New password: ")

        self.HashMethod = hashlib.sha256()
        self.HashMethod.update(OldPassword.encode())
        OldHash = (self.HashMethod.hexdigest()).upper()
        self.HashMethod = hashlib.sha256()
        self.HashMethod.update(NewPassword.encode())
        NewHash = (self.HashMethod.hexdigest()).upper()

        return {'Action': 'ChangePassword', 'Args': {'Login': Login, 'OldPassword': OldHash, 'NewPassword': NewHash}}

    def AddToGroup(self):
        GroupName = input('GroupName: ')
        User = input('User login: ')
        Function = input('Function [User/Administrator]: ')

        return {'Action': 'AddToGroup', 'Args': {'GroupName': GroupName, 'UserLogin': User, 'FunctionName': Function}}

    def CreateTask(self):
        GroupName = input('GroupName: ')
        TaskTitle = input('Title: ')
        Desc = input("Description: ")

        return {'Action': 'CreateTask',
                'Args': {'GroupName': GroupName, 'Title': TaskTitle, 'Description': Desc, 'State': 10,
                         'Localisation': '...'}}

    def CreateSubTask(self):
        TaskTitle = input('TaskTitle: ')
        User = input('User: ')
        Desc = input("Description: ")

        return {'Action': 'CreateSubTask',
                'Args': {'TaskTitle': TaskTitle, 'Description': Desc, 'User': User, 'State': 10,
                         'Localisation': '...'}}

    def CreateGroup(self):
        GroupName = input('GroupName: ')

        return {'Action': 'CreateGroup', 'Args': {'GroupName': GroupName}}

    def DeleteGroup(self):
        GroupName = input('GroupName: ')

        return {'Action': 'DeleteGroup', 'Args': {'GroupName': GroupName}}

    def DisplayGroups(self):
        return {'Action': 'ShowGroups'}

    def DisplayUsers(self):
        GroupName = input('GroupName: ')

        return {'Action': 'ShowUsers', 'Args': {'GroupName': GroupName}}

    def DisplayTasks(self):
        GroupName = input('GroupName: ')

        return {'Action': 'ShowTask', 'Args': {'GroupName': GroupName}}

    def DisplaySubTasks(self, Title):
        return {'Action': 'ShowSubTask', 'Args': {'TaskTitle': Title}}

    def ChangeTaskStatus(self):
        TaskTitle = input("TaskTitle: ")
        SubTaskNumber = input("Number: ")
        State = input("State: ")

        return {'Action': 'ChangeTaskStatus',
                'Args': {'TaskTitle': TaskTitle, 'SubTaskNumber': SubTaskNumber, 'State': State}}

    def LeaderView(self):
        Login = input("Login: ")

        return {'Action': 'LeaderView', 'Args': {'Login': Login}}

    def ResetPassword(self):
        Email = input("Email: ")

        return {'Action': 'ResetPassword', 'Args': {'Email': Email}}


class ClientInterface:
    def __init__(self):
        self.Actions = {
            1: "Create user",
            2: "Login",
            3: "Change password",
            4: "Create group",
            5: "Delete group",
            6: "Add to group",
            7: "Show groups",
            8: "Show users",
            9: "Create task",
            10: "Create subtask",
            11: "Show tasks",
            12: "ChangeTaskStatus",
            13: "Leader view",
            14: "Resert password",
            15: "Exit"
        }
        self.Client = SocketClient.Client()
        self.Queries = ClientQuery()

    def Menu(self):
        for k in self.Actions:
            print("{0}. {1}".format(k, self.Actions[k]))

        Choice = input("What you want to do: ")
        if not self.isINT(Choice):
            print("This is not a number! Try again!")
            input("Press ENTER to continue...")
            os.system("clear")
            self.Menu()
        self.ManageOperations(int(Choice))

    def ManageOperations(self, Operation):
        Mode = None
        if Operation == 1:
            Mode = "Flag"
            Send = self.Queries.CreateUser()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 2:
            Mode = "Flag"
            Send = self.Queries.Login()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 3:
            Mode = "Flag"
            Send = self.Queries.ChangePassword()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 4:
            Mode = "Flag"
            Send = self.Queries.CreateGroup()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 5:
            Mode = "Flag"
            Send = self.Queries.DeleteGroup()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 6:
            Mode = "Flag"
            Send = self.Queries.AddToGroup()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 7:
            Mode = "Table-Groups"
            Send = self.Queries.DisplayGroups()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 8:
            Mode = "Table-Users"
            Send = self.Queries.DisplayUsers()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode, Send['Args']['GroupName'])
        elif Operation == 9:
            Mode = "Flag"
            Send = self.Queries.CreateTask()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 10:
            Mode = "Flag"
            Send = self.Queries.CreateSubTask()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 11:
            Mode = "Table-Task"
            Send = self.Queries.DisplayTasks()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 12:
            Mode = "Flag"
            Send = self.Queries.ChangeTaskStatus()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 13:
            Mode = "Flag"
            Send = self.Queries.LeaderView()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 14:
            Mode = "Flag"
            Send = self.Queries.ResetPassword()
            Recieve = self.Client.ProcessEvent(Send)
            self.Display(Recieve, Mode)
        elif Operation == 15:
            exit()
        else:
            print("Error! There is not such option!")

    def Display(self, DataToDisplay, Mode, Suplementary=None):
        if isinstance(DataToDisplay, list):
            if Mode == "Flag":
                print(DataToDisplay[0])
            elif Mode == "Table-Groups":
                Table = PrettyTable(["Group name"])
                for Group in DataToDisplay:
                    Table.add_row([Group])
                print(Table)
            elif Mode == "Table-Users":
                Table = PrettyTable(['Login', 'First name', 'Last name', 'Email', 'Group'])
                for User in DataToDisplay:
                    Table.add_row([User['Login'], User['FirstName'], User['LastName'], User['Email'],
                                   User['GroupName'] if 'GroupName' in User else Suplementary])
                print(Table)
            elif Mode == "Table-Task":
                TaskTable = PrettyTable(['Title', 'Description', 'Status'])
                TaskTitles = []
                for Task in DataToDisplay:
                    print(Task['Progress'])
                    print("########### Progress: {0} ###########".format(Task['Progress']))
                    TaskTitles.append(Task['Title'])
                    TaskTable.add_row([Task['Title'], Task['Description'], Task['State']])
                print(TaskTable)
                SubTaskTable = PrettyTable(['Main task title', 'Description', 'User', 'Status'])
                for Title in TaskTitles:
                    Send = self.Queries.DisplaySubTasks(Title)
                    Recieve = self.Client.ProcessEvent(Send)
                    if isinstance(Recieve[0], dict):
                        for SubTask in Recieve:
                            SubTaskTable.add_row([Title, SubTask['Description'], SubTask['User'], SubTask['State']])
                print(SubTaskTable)
        else:
            print("Data type error!")

    def isINT(self, Value):
        try:
            int(Value)
            return True
        except ValueError:
            return False
