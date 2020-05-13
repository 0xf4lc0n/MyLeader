import mysql.connector
import bcrypt
from random import choice
from string import ascii_letters, digits, punctuation
from eMail import Mail
from AuthTime import Auth, Manager, ThreadStore


class DataBaseOperate:
    def __init__(self):
        ThreadManager = Manager()
        ThreadManager.start()
        # Connection details
        self.ConnDet = [{
            'user': 'Conn',
            'password': 'ConnP',
            'host': '192.168.100.45',
            'database': 'MyLeader',
            'connection_timeout': 10
        },

            {
                'user': 'Conn',
                'password': 'ConnP',
                'host': '192.168.100.45',
                'database': 'Salt',
                'connection_timeout': 10
            }]

    def CreateUser(self, DictArg):
        """
        Creating user
        :param DictArg:
        {'Operation': 'CreateUser', 'Args': {'Login': '...', 'Password': '...', 'FirstName': '...',
        'LastName': '...', 'Email': '...'}}
        :return: Status code
        """
        # Checking if user exist
        if self.ElementExist(DictArg['Args']['Login'], 'Accounts', 'Login') or \
                self.ElementExist(DictArg['Args']['Email'], 'Users', 'Email'):
            return [130]
        try:
            # Data section
            Salt = self.GenerateSalt().decode()
            Pass = (self.GeneratePass(DictArg['Args']['Password'], Salt)).decode()

            AccountQuery = "INSERT INTO Accounts(ID, Login) VALUES(null, '{0}')".format(DictArg['Args']['Login'])

            UserQuery = "INSERT INTO Users(ID, AccountID, FirstName, LastName, Email, Password, SaltID) " \
                        "VALUES(null, {0}, '{1}', '{2}', '{3}', '{4}', {5})"
            UserQuery = UserQuery.format(self.LastIndex(self.ConnDet[0], "Accounts"), DictArg['Args']['FirstName'],
                                         DictArg['Args']['LastName'], DictArg['Args']['Email'], Pass,
                                         self.LastIndex(self.ConnDet[1], "Salts"))

            SaltQuery = "INSERT INTO Salts(ID, Salt) VALUES(null, '{0}')".format(Salt)

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            SaltDB = mysql.connector.connect(**self.ConnDet[1])

            LeaderOperate = MyLeaderDB.cursor()
            SaltOperate = SaltDB.cursor()

            # Sending queries
            LeaderOperate.execute(AccountQuery)
            MyLeaderDB.commit()

            LeaderOperate.execute(UserQuery)
            MyLeaderDB.commit()

            SaltOperate.execute(SaltQuery)
            SaltDB.commit()

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()
            SaltDB.close()
            SaltOperate.close()

            return [0]
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def ShowUsers(self, DictArg):
        """
        Downloading all users for group or whole application instance
        :param DictArg:
        {'Action': 'ShowUsers', 'Args': {'GroupName': '...'}}
        :return: Users' list or status code
        """
        try:
            # Data section
            Users = []

            if DictArg['Args']['GroupName'] == '':
                ShowQuery = "SELECT Login, FirstName, LastName, Email FROM Users " \
                            "JOIN Accounts ON Accounts.ID = Users.AccountID "
                GroupQuery = "SELECT GroupName FROM Groups INNER JOIN Membership ON Groups.ID = Membership.GroupID " \
                             "WHERE Membership.AccountID = {0}"
                Mode = 'P'
            else:
                ShowQuery = "SELECT Login, FirstName, LastName, Email FROM Membership JOIN Users " \
                            "ON Membership.AccountID = Users.AccountID JOIN Groups ON Membership.GroupID = Groups.ID " \
                            "JOIN Accounts ON Membership.AccountID = Accounts.ID  WHERE GroupName = '{0}'"
                ShowQuery = ShowQuery.format(DictArg['Args']['GroupName'])
                Mode = 'N'

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(ShowQuery)

            # Preparing result list
            if Mode == 'P':
                # Admin
                for Res in LeaderOperate:
                    UserDict = dict(Login=Res[0], FirstName=Res[1], LastName=Res[2], Email=Res[3])
                    Users.append(UserDict)

                CopyUsers = Users
                Users = []

                for User in CopyUsers:
                    UserID = self.DownloadID(User['Login'], 'Accounts', 'Login')
                    Query = GroupQuery.format(UserID)

                    # Sending query
                    LeaderOperate.execute(Query)
                    Counter = 0

                    for Group in LeaderOperate:
                        UserDict = dict(Login=User['Login'], FirstName=User['FirstName'], LastName=User['LastName'],
                                        Email=User['Email'], GroupName=Group[0])
                        Users.append(UserDict)
                        Counter += 1

                    if Counter == 0:
                        UserDict = dict(Login=User['Login'], FirstName=User['FirstName'], LastName=User['LastName'],
                                        Email=User['Email'], GroupName='None')
                        Users.append(UserDict)

            else:
                # Normal user
                for User in LeaderOperate:
                    UserDict = dict(Login=User[0], FirstName=User[1], LastName=User[2], Email=User[3])
                    Users.append(UserDict)

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            # Checking if any users were returned
            if len(Users) == 0:
                return [115]
            else:
                return Users
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def Login(self, DictArg):
        """
        Logging
        :param DictArg:
        {'Action': 'Login', 'Args': {'Login': '...', 'Password': '...'}}
        :return: Status code
        """
        try:
            # Data section
            LoginQuery = "SELECT Login, Password, SaltID, Activated FROM Accounts INNER JOIN Users ON " \
                         "Users.AccountID=Accounts.ID WHERE Login='{0}'".format(DictArg['Args']['Login'])
            SaltQuery = "SELECT Salt FROM Salts WHERE ID = {0}"

            SaltID = None
            Salt = None
            Hash = None
            Active = None

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(LoginQuery)

            # Saving password hash, salt ID and account activation flag
            for Res in LeaderOperate:
                Hash = Res[1]
                SaltID = Res[2]
                Active = Res[3]

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            # Checking if account was activated
            if Active == 0:
                return [140]

            # Starting connection
            SaltDB = mysql.connector.connect(**self.ConnDet[1])
            SaltOperate = SaltDB.cursor()

            # Modifying and sending query
            SaltQuery = SaltQuery.format(SaltID)
            SaltOperate.execute(SaltQuery)

            # Saving salt
            for Res in SaltOperate:
                Salt = Res[0]

            # Closing connection
            SaltDB.close()
            SaltOperate.close()

            # Checking if salt exist
            if Salt is None:
                Flag = 120
            else:
                # Generate password hash
                Pass = (self.GeneratePass(DictArg['Args']['Password'], Salt)).decode()
                # Checking if generated password's hash is equal to hash placed in database
                if Pass == Hash:
                    print("Logged successful!")
                    Flag = 0
                else:
                    print("Error! Logged unsuccessful. Authentication refused!")
                    Flag = 120
            return [Flag]
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def ChangePassword(self, DictArg):
        """
        Changing user password
        :param DictArg:
        {'Action': 'ChangePassword', 'Args': {'Login': '...', 'OldPassword': '...', 'NewPassword': '...'}}
        :return: Status code
        """

        # Data section
        LoginDict = {'Action': 'Login', 'Args':
            {'Login': DictArg['Args']['Login'], 'Password': DictArg['Args']['OldPassword']}}
        SelectQuery = "SELECT SaltID FROM Users WHERE AccountID = {0}"
        ChangePassQuery = "UPDATE Users SET Password = '{0}' WHERE AccountID = {1}"
        ChangeSaltQuery = "UPDATE Salts SET Salt = '{0}' WHERE ID = {1}"

        # Checking if entered data are correct
        if self.Login(LoginDict)[0] == 0:
            # Generating new salt
            Salt = self.GenerateSalt().decode()
            # Creating password hash
            Pass = (self.GeneratePass(DictArg['Args']['NewPassword'], Salt)).decode()
            # Downloading user ID
            UserID = self.DownloadID(DictArg['Args']['Login'], "Accounts", "Login")
            SaltID = None

            try:
                # Starting connection
                MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
                LeaderOperate = MyLeaderDB.cursor()

                # Modifying and sending query
                SelectQuery = SelectQuery.format(UserID)
                LeaderOperate.execute(SelectQuery)

                # Saving salt ID
                for Res in LeaderOperate:
                    SaltID = Res[0]

                # Modifying and sending query
                ChangePassQuery = ChangePassQuery.format(Pass, UserID)
                LeaderOperate.execute(ChangePassQuery)
                MyLeaderDB.commit()

                # Closing connection
                MyLeaderDB.close()
                LeaderOperate.close()

                # Starting connection
                SaltDB = mysql.connector.connect(**self.ConnDet[1])
                SaltOperate = SaltDB.cursor()

                # Modifying and sending query
                ChangeSaltQuery = ChangeSaltQuery.format(Salt, SaltID)
                SaltOperate.execute(ChangeSaltQuery)
                SaltDB.commit()

                # Closing connection
                SaltDB.close()
                SaltOperate.close()

                return [0]
            except mysql.connector.Error as err:
                print("Error: ", err)
                if err.errno == 2003:
                    return [50]
                elif err.errno == 1049:
                    print("Unknown database: ", self.ConnDet[0]['database'])
                    return [55]
                else:
                    return [300]
            except KeyError as er:
                print(er)
                return [100]
        else:
            return [125]

    def ResetPassword(self, DictArg):
        """
        Reset password if user don't remember the old one.
        Setting reset flag in database and creating new, temporary password.
        Sending email with generated password, creating file which store user ID.
        Running threat which count reset time down.
        :param DictArg:
        {'Action': 'ResetPassword', 'Args': {'Email': '...'}}
        :return: Status code
        """

        # Data section
        Counter = 0
        UserData = None
        NewPass = ""

        SelectQuery = "SELECT Accounts.ID, Login FROM Accounts INNER JOIN Users ON Users.AccountID = Accounts.ID " \
                      "WHERE Email = '{0}'"
        SelectQuery = SelectQuery.format(DictArg['Args']['Email'])

        SetFlagQuery = "UPDATE Users SET Reset = 1 WHERE AccountID = '{0}'"

        # Starting connection
        try:
            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(SelectQuery)

            # Saving user ID and Login to dictionary
            for Res in LeaderOperate:
                UserData = dict(ID=Res[0], Login=Res[1])
                Counter += 1
            # If none records were returned close connection and return error code
            if Counter == 0:
                MyLeaderDB.close()
                LeaderOperate.close()
                return [110]
            # If more than one record were returned close connection and return error code
            elif Counter > 1:
                MyLeaderDB.close()
                LeaderOperate.close()
                return [300]

            # Preparing query
            SetFlagQuery = SetFlagQuery.format(UserData['ID'])

            # Sending query
            LeaderOperate.execute(SetFlagQuery)
            MyLeaderDB.commit()

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            # Generating new password
            NewPass = NewPass.join((choice(ascii_letters + digits + punctuation) for n in range(0, 30)))

            # Sending mail to client
            MailService = Mail(DictArg['Args']['Email'])
            Mail.CreateMessage(MailService, NewPass)
            MailService.SendMail()

            AuthService = Auth(UserData['ID'], UserData['Login'])
            AuthService.CreateFile(NewPass)
            AuthService.start()
            ThreadStore.append(AuthService)

            return [0]

        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def ProceedReset(self):
        pass

    def CreateTask(self, DictArg):
        """
        Creating task
        :param DictArg:
        {'Action': 'CreateTask', 'Args': {'GroupName': '...', 'Title': '...', 'Description': '...', 'State': '...',
        'Localisation': '...'}}
        :return: Status code
        """
        try:
            # Data section
            CreateQuery = "INSERT INTO Tasks (ID, GroupID, Title, Description, StateID, Localisation) " \
                          "VALUES(null, {0}, '{1}', '{2}', {3}, '{4}')"
            CreateQuery = CreateQuery.format(self.DownloadID(DictArg['Args']['GroupName'], 'Groups', 'GroupName'),
                                             DictArg['Args']['Title'], DictArg['Args']['Description'],
                                             DictArg['Args']['State'], DictArg['Args']['Localisation'])

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(CreateQuery)
            MyLeaderDB.commit()

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            return [0]
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def ShowTask(self, DictArg):
        """
        Downloading all tasks for Group
        :param DictArg:
        {'Action': 'ShowTask', 'Args': {'GroupName': '...'}}
        :return: Tasks' list or status code
        """
        try:
            # Data section
            Tasks = []

            ShowQuery = "SELECT Title, Description, StateID FROM Tasks WHERE GroupID = '{0}'"
            ShowQuery = ShowQuery.format(self.DownloadID(DictArg['Args']['GroupName'], 'Groups', 'GroupName'))

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(ShowQuery)

            # Preparing tasks list
            for Res in LeaderOperate:
                Status = self.DownloadElement(Res[2], 'TaskStates', 'TaskState', self.ConnDet[0])
                TaskDict = dict(Title=Res[0], Description=Res[1], State=Status, Progress=self.Progress(Res[0]))
                Tasks.append(TaskDict)

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            # Checking if any tasks were returned
            if len(Tasks) == 0:
                return [115]
            else:
                return Tasks
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def CreateSubTask(self, DictArg):
        """
        Creating sub task
        :param DictArg:
        {'Action': 'CreateSubTask', 'Args': {'TaskTitle': '...', 'Description': '...', 'User': '...', 'State': '...',
        'Localisation': '...'}}
        :return: Status code
        """
        try:
            # Data section
            CreateQuery = "INSERT INTO SubTasks (ID, TaskID, Description, AccountID, StateID, Localisation) " \
                          "VALUES(null, {0}, '{1}', '{2}', {3}, '{4}')"
            CreateQuery = CreateQuery.format(self.DownloadID(DictArg['Args']['TaskTitle'], 'Tasks', 'Title'),
                                             DictArg['Args']['Description'],
                                             self.DownloadID(DictArg['Args']['User'], 'Accounts', 'Login'),
                                             DictArg['Args']['State'], DictArg['Args']['Localisation'])

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(CreateQuery)
            MyLeaderDB.commit()

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            return [0]
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def ShowSubTask(self, DictArg):
        """
        Downloading sub tasks for specifeid task
        :param DictArg:
        {'Action': 'ShowSubTask', 'Args': {'TaskTitle': '...'}
        :return: Sub tasks' list or status code
        """
        try:
            # Data section
            SubTasks = []

            CreateQuery = "SELECT Description, AccountID, StateID FROM SubTasks WHERE TaskID = {0}"
            CreateQuery = CreateQuery.format(self.DownloadID(DictArg['Args']['TaskTitle'], 'Tasks', 'Title'))

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(CreateQuery)

            # Preparing sub task list
            for Res in LeaderOperate:
                Login = self.DownloadElement(Res[1], 'Accounts', 'Login', self.ConnDet[0])
                Status = self.DownloadElement(Res[2], 'TaskStates', 'TaskState', self.ConnDet[0])
                SubTaskDict = dict(Description=Res[0], User=Login, State=Status)
                SubTasks.append(SubTaskDict)

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            # Checking if any sub tasks were returned
            if len(SubTasks) == 0:
                return [115]
            else:
                return SubTasks
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def ChangeTaskStatus(self, DictArg):
        """
        Changin task status ex. from "Created" to "Finished" etc
        :param DictArg:
        {'Action': 'ChangeTaskStatus', 'Args': {'TaskTitle': '...', 'SubTaskNumber': '...', 'State': '...'}}
        :return: Status code
        """

        try:
            # Data section
            TaskID = self.DownloadID(DictArg['Args']['TaskTitle'], "Tasks", "Title")
            StateID = DictArg['Args']['State'] if self.isINT(DictArg['Args']['State']) else \
                self.DownloadID(DictArg['Args']['State'], "TaskStates", "TaskState")
            UpdateTaskQuery = "UPDATE {0} SET StateID = {1} WHERE ID = {2}"
            SubTaskID = 0

            # Checking if chosen task and state exist
            if TaskID == 0 or StateID == 0:
                return [300]

            # Checking if sub task wasn't chosen
            if DictArg['Args']['SubTaskNumber'] == '-1':
                # True: prepare query for main task
                UpdateTaskQuery = UpdateTaskQuery.format("Tasks", StateID, TaskID)
            else:
                # False: prepare query for sub task
                SubTaskID = self.DownloadSubTaskID(TaskID, DictArg['Args']['SubTaskNumber'])
                # Checking if sub task exist
                if SubTaskID == 0:
                    return [135]
                else:
                    UpdateTaskQuery = UpdateTaskQuery.format("SubTasks", StateID, SubTaskID)

            # Starting connection
            MyLeader = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeader.cursor()

            # Sending query
            LeaderOperate.execute(UpdateTaskQuery)
            MyLeader.commit()

            # Closing connection
            MyLeader.close()
            LeaderOperate.close()

            return [0]
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def CreateGroup(self, DictArg):
        """
        Creating group
        :param DictArg:
        {'Action': 'CreateGroup', Args: {'GroupName': '...'}}
        :return: Status code
        """

        if DictArg['Args']['GroupName'] == "None":
            return [110]

        if self.ElementExist(DictArg['Args']['GroupName'], 'Groups', 'GroupName'):
            return [110]

        try:
            # Data section
            CreateQuery = "INSERT INTO Groups(ID, GroupName) VALUES(null , '{0}')".format(DictArg['Args']['GroupName'])

            # Starting connection
            MyLeader = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeader.cursor()

            # Sending query
            LeaderOperate.execute(CreateQuery)
            MyLeader.commit()

            # Closing connection
            MyLeader.close()
            LeaderOperate.close()

            return [0]
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as err:
            print(err)
            return [100]

    def DeleteGroup(self, DictArg):
        """
        Deleting specified group
        :param DictArg:
        {'Action': 'DeleteGroup', 'Args': {'GroupName': '...'}}
        :return: Status code
        """
        try:
            # Data section
            DeleteQuery = "DELETE FROM Groups WHERE GroupName = '{0}'".format(DictArg['Args']['GroupName'])

            # Starting connection
            MyLeader = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeader.cursor()

            # Sending query
            LeaderOperate.execute(DeleteQuery)
            MyLeader.commit()

            # Closing connection
            MyLeader.close()
            LeaderOperate.close()

            return [0]
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def AddToGroup(self, DictArg):
        """
        Adding user to group and giving him function
        :param DictArg:
        {'Action': 'AddToGroup', 'Args': {'GroupName': '...', 'UserLogin': '...', 'FunctionName': '...'}}
        :return: Status code
        """
        try:
            # Data section
            GroupName = DictArg['Args']['GroupName']
            User = DictArg['Args']['UserLogin']
            Function = DictArg['Args']['FunctionName']
            GroupID = self.DownloadID(GroupName, 'Groups', 'GroupName')
            UserID = self.DownloadID(User, 'Accounts', 'Login')
            FunctionID = DictArg['Args']['FunctionName'] if self.isINT(DictArg['Args']['FunctionName']) \
                else self.DownloadID(Function, 'Functions', 'FunctionName')
            AddQuery = "INSERT INTO Membership (ID, GroupID, AccountID, FunctionID) VALUES (null, {0}, {1}, {2})"

            # Checking if data was properly loaded (if not variable = 0 otherwise variable = 1)
            if GroupID and UserID and FunctionID:
                # Starting connection
                MyLeader = mysql.connector.connect(**self.ConnDet[0])
                LeaderOperate = MyLeader.cursor()

                # Modifying and sending query
                AddQuery = AddQuery.format(GroupID, UserID, FunctionID)
                LeaderOperate.execute(AddQuery)
                MyLeader.commit()

                # Closing connection
                MyLeader.close()
                LeaderOperate.close()

                return [0]
            else:
                return [110]
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def ShowGroups(self, DictArg):
        """
        Downloading all available groups
        :param DictArg:
        {'Action': 'ShowGroups', 'Args': {'GroupName': '...'}}
        :return: Groups list or status code
        """
        try:
            # Data section
            Groups = []
            SelectQuery = "SELECT GroupName FROM Groups"

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(SelectQuery)

            # Preparing groups list
            for Res in LeaderOperate:
                Groups.append(Res[0])

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            # Checking if any groups were returned
            if len(Groups) == 0:
                return [115]
            else:
                return Groups
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def LeaderView(self, DictArg):
        """
        Downloading:
        - groups, where specified user is set as Administrator
        - tasks for each groups
        Calculate the number of finished and unfinished tasks.
        :param DictArg: {'Action': 'LeaderView', 'Args': {'Login': '...'}}
        :return:
        """

        try:
            # Data section
            Groups = []
            Result = []
            SelectQuery = "SELECT GroupName FROM Membership JOIN Groups ON Membership.GroupID = Groups.ID " \
                          "JOIN Accounts ON Membership.AccountID = Accounts.ID WHERE Login = '{0}' AND FunctionID = 5"
            SelectQuery = SelectQuery.format(DictArg['Args']['Login'])

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(SelectQuery)

            # Saving returned groups
            for Res in LeaderOperate:
                Groups.append(Res[0])

            # Checking if any groups were returned
            if len(Groups) == 0:
                MyLeaderDB.close()
                LeaderOperate.close()
                return [115]

            # Downloading tasks for each group
            for Group in Groups:
                Tasks = self.ShowTask({'Action': 'ShowTask', 'Args': {'GroupName': Group}})

                # Setting counters to 0
                Fin = 0
                nFin = 0
                inProg = 0

                # Calculating
                for Task in Tasks:
                    if type(Task) is dict:
                        if Task['Progress'] == 0.0:
                            nFin += 1
                        elif Task['Progress'] == 100.0:
                            Fin += 1
                        elif Task['Progress'] > 0.0 and Task['Progress'] < 100.0:
                            inProg += 1

                # Creating dictiorany and adding to list
                Result.append(dict(GroupName=Group, Finished=Fin, NotFinished=nFin, InProgress=inProg))

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            return Result

        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def DisableResetFlag(self, Login):
        # Data section
        UserID = self.DownloadID(Login, "Accounts", "Login")
        SetFlagQuery = "UPDATE Users SET Reset = 0 WHERE AccountID = '{1}'"
        SetFlagQuery = SetFlagQuery.format(UserID)

        try:
            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(SetFlagQuery)
            MyLeaderDB.commit()

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]

    # Additional/Supplementary methods

    def Progress(self, TaskTitle):
        """
        Function returning progress for specified task
        :param DictArg:
        {'Action': 'Progress', 'Args': {'TaskTitle': '...'}}
        :return: Percent value
        """
        try:
            # Data section
            SelectTaskQuery = "SELECT ID, StateID FROM Tasks WHERE Title = '{0}'".format(TaskTitle)
            SelectSubTaskQuery = "SELECT StateID FROM SubTasks WHERE TaskID = {0}"
            TaskID = 0
            StateID = 0
            Counter = 0
            Finished = 0
            inProgress = 0

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(SelectTaskQuery)

            # Saving task and state IDs
            for Res in LeaderOperate:
                TaskID = Res[0]
                StateID = Res[1]

            # Checking if main task was finished
            if StateID == 40:
                return 100

            # Modifying and sending quey
            SelectSubTaskQuery = SelectSubTaskQuery.format(TaskID)
            LeaderOperate.execute(SelectSubTaskQuery)

            # Checking sub tasks
            for Res in LeaderOperate:
                Counter += 1
                if Res[0] == 30:
                    inProgress += 1
                elif Res[0] == 40:
                    Finished += 1

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            # Checking if any sub task was returned
            if Counter == 0:
                return 0
            else:
                # Calculating progress
                Progress = round(Finished / Counter, 2)
                return Progress

        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return [50]
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return [55]
            else:
                return [300]
        except KeyError as er:
            print(er)
            return [100]

    def ElementExist(self, Value, Table, Column):
        """
        Checking if specified Value exist in Table
        SELECT Column FROM Table WHERE Column = 'Value'
        :param Value:
        :param Table:
        :param Column:
        :return: 1 if exist, 0 otherwise
        """
        try:
            # Data section
            CheckQuery = "SELECT {2} FROM {1} WHERE {2}='{0}'".format(Value, Table, Column)
            bState = None

            # Starting connection
            MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
            LeaderOperate = MyLeaderDB.cursor()

            # Sending query
            LeaderOperate.execute(CheckQuery)

            # Checking if specified value exist in table and setting flag
            for Res in LeaderOperate:
                if Res[0] == Value:
                    bState = 1
                else:
                    bState = 0

            # Closing connection
            MyLeaderDB.close()
            LeaderOperate.close()

            return bState
        except mysql.connector.Error as err:
            print("Error: ", err)
            if err.errno == 2003:
                return "Can't connect to database server! Contact with network administrator!"
            elif err.errno == 1049:
                print("Unknown database: ", self.ConnDet[0]['database'])
                return "Database server error! Contact with technical department!"
            else:
                return "Unexpected error! Contact with technical department!"
        except Exception as err:
            print("Error: ", err)
            return "Unexpected error! Contact with technical department!"

    def DownloadID(self, Value, Table, Column):
        """
        Downloading ID of specified Value from Table
        :param Value:
        :param Table:
        :param Column:
        :return: False if ID is 0 (Value does't exist), otherwise ID
        """

        # Data section
        QueryID = "SELECT ID FROM {0} WHERE {1} = '{2}'".format(Table, Column, Value)
        ID = 0

        # Starting connection
        MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
        LeaderOperate = MyLeaderDB.cursor()

        # Sending query
        LeaderOperate.execute(QueryID)

        # Saving ID
        for Res in LeaderOperate:
            ID = Res[0]

        # Closing connection
        MyLeaderDB.close()
        LeaderOperate.close()

        # Checking if ID was changed (returned)
        if ID == 0:
            return False
        else:
            return ID

    def DownloadSubTaskID(self, TaskID, Number):
        """
        Downloading ID of specified sub task
        :param TaskID:
        :param Number:
        :return: Sub task ID
        """

        # Data section
        Query = "SELECT ID FROM (SELECT ID FROM SubTasks WHERE TaskID = {0} LIMIT {1},1) AS TB".format(TaskID, Number)
        ID = 0

        # Starting connection
        MyLeaderDB = mysql.connector.connect(**self.ConnDet[0])
        LeaderOperate = MyLeaderDB.cursor()

        # Sending query
        LeaderOperate.execute(Query)

        # Saving ID
        for Res in LeaderOperate:
            ID = Res[0]

        # Closing connection
        MyLeaderDB.close()
        LeaderOperate.close()

        # Checking if ID was changed (returned)
        if ID == 0:
            return False
        else:
            return ID

    def DownloadElement(self, Value, Table, Column, Database):
        """
        Downloading element from Table via ID
        :param Value:
        :param Table:
        :param Column:
        :param Database:
        :return: Wanted Value or exception if index error occur
        """

        # Data section
        iCounter = 0
        DownloadValue = None
        QueryID = "SELECT {0} FROM {1} WHERE ID = {2}".format(Column, Table, Value)

        # Starting connection
        MyLeaderDB = mysql.connector.connect(**Database)
        LeaderOperate = MyLeaderDB.cursor()

        # Sending query
        LeaderOperate.execute(QueryID)

        # Saving downloaded element
        for Res in LeaderOperate:
            iCounter += 1
            DownloadValue = Res[0]

        # Closing connection
        MyLeaderDB.close()
        LeaderOperate.close()

        # Checking if more than one element was downloaded
        if iCounter == 1:
            return DownloadValue
        else:
            raise Exception("Index error!")

    def LastIndex(self, Database, Table):
        """
        Downloading last index from specified Table
        :param Database:
        :param Table:
        :return: ID of last record
        """

        # Data section
        IndexQuery = "SELECT ID FROM {0} ORDER BY ID DESC LIMIT 1".format(Table)
        LastID = 1

        # Starting connection
        MyLeaderDB = mysql.connector.connect(**Database)
        LeaderOperate = MyLeaderDB.cursor()

        # Sending query
        LeaderOperate.execute(IndexQuery)

        # Saving downloaded ID
        for Res in LeaderOperate:
            LastID = Res[0] + 1

        # Closing connection
        MyLeaderDB.close()
        LeaderOperate.close()

        return LastID

    def GenerateSalt(self):
        """
        Generating salt
        :return: Salt
        """
        return bcrypt.gensalt()

    def GeneratePass(self, Pass, Salt):
        """
        Generating password
        :param Pass:
        :param Salt:
        :return: Password hash
        """
        Result = (Salt + Pass + Salt).encode()
        Result = bcrypt.hashpw(Result, Salt.encode())
        Result = Result[7:]
        return Result

    def isINT(self, Value):
        try:
            int(Value)
            return True
        except ValueError:
            return False
