# MyLeader
This is MyLeader's server which I developed for competitions related purposes. Server cooperated with aplication dedicated for
Android system but I was responsible only for server side stuff and I don't own the Android app, so I can't publish it here.

MyLeader was dedicated for managing tasks and responsibilities across people who work in groups. Basically MyLeader was supposed to
be much simpler version of Trello distributed as open source software. However, the project has been abandoned and will no
longer be developed.

I also developed simple client that allowed me to test server features.

```diff
- Please, don't use that code in a production environment or in place where any security standards are desired. 
```
This code is a bit messy and there are some awful solutions e.x. password reset or hard-coded credentials.

## Geting started
If there is any reason for you to start this server you must follow this steps.

### Prerequisites

##### MySQL
You will need a MySQL database which will be hosted by server (you can use Docker, VM or whatever you want). Install MySQL and
configure it properly, then import databases which are in this repository.
Create database user and give him permissions  to modify those two databases.

On the end of this step, you can check if your database port is open (it's 3306 port). In order to do this you can use nmap.

##### Server
You have to change database connection settings. In order to do this open file DatabaseQuery.py and modify ConnDet list which is placed in DataBaseOperate class.

```python
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
```

Change the "user" and "password" values to match the user you created. 
Set "host" value to address of your machine which running MySQL server.
Set "database" value to match the name of two imported databases.

##### Requirements
Use requirements.txt to install all required libraries.

### Let's run it
If everything is ready you can start server.

```diff
python3 Server.py
```

By default server will listen on 127.0.0.1:8010.
You can change IP and port by specyfying this in command's arguments.

```diff
python3 Server.py 192.168.100.50 3050
```

Analogically you can start client.

```diff
python3 Client.py
```

By default client will connect to server running on 127.0.0.1:8010.
You can change IP and port by specyfying this in command's arguments.

```diff
python3 Client.py 192.168.100.50 3050
```
