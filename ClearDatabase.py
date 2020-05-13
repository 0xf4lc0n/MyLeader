import mysql.connector

ConnDet = [{
    'user': 'Conn',
    'password': 'ConnP',
    'host': '192.168.1.45',
    'database': 'MyLeader'
},

{
    'user': 'Conn',
    'password': 'ConnP',
    'host': '192.168.1.45',
    'database': 'Salt'
}]

CleanMembership = "DELETE FROM Membership WHERE ID != 0"
SetMembership = "ALTER TABLE Membership AUTO_INCREMENT = 1"

CleanUser = "DELETE FROM Users WHERE ID != 0"
SetUser = "ALTER TABLE Users AUTO_INCREMENT = 1"

CleanAccount = "DELETE FROM Accounts WHERE ID != 0"
SetAccount = "ALTER TABLE Accounts AUTO_INCREMENT = 1"

CleanSalt = "DELETE FROM Salts WHERE ID != 0"
SetSalt = "ALTER TABLE Salts AUTO_INCREMENT = 1"

CleanSubTask = "DELETE FROM SubTasks WHERE ID != 0"
SetSubTask = "ALTER TABLE SubTasks AUTO_INCREMENT = 1"

CleanTask = "DELETE FROM Tasks WHERE ID != 0"
SetTask = "ALTER TABLE Tasks AUTO_INCREMENT = 1"

CleanGroups = "DELETE FROM Groups WHERE ID != 0"
SetGroups = "ALTER TABLE Groups AUTO_INCREMENT = 1"

MyL = mysql.connector.connect(**ConnDet[0])
MyL_Curs = MyL.cursor()

MyL_Curs.execute(CleanMembership)
MyL_Curs.execute(SetMembership)
MyL_Curs.execute(CleanSubTask)
MyL_Curs.execute(SetSubTask)
MyL_Curs.execute(CleanTask)
MyL_Curs.execute(SetTask)
MyL_Curs.execute(CleanGroups)
MyL_Curs.execute(SetGroups)
MyL_Curs.execute(CleanUser)
MyL_Curs.execute(SetUser)
MyL_Curs.execute(CleanAccount)
MyL_Curs.execute(SetAccount)

MyL.commit()
MyL.close()
MyL_Curs.close()

Sal = mysql.connector.connect(**ConnDet[1])
Sal_Curs = Sal.cursor()

Sal_Curs.execute(CleanSalt)
Sal_Curs.execute(SetSalt)

Sal.commit()
Sal.close()
Sal_Curs.close()
