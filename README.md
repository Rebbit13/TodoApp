This is a test web service for todo list
---
You can create todos, reed, update, delete them within an API.

Project uses
---
- Python 3.9.1 (you should use python > 3.9)
- Flask as a core module
- flask-restx as a module to build CRUD API
- peewee as an ORM for SQLite 3

Modules
---
- main - process requests to a server. You can try paths after running the app 
  and go to domain path.
  * "api/task" - the path to GET list of all tasks and POST new task.
  * "api/task/{task_id}" - the path to GET concrete task, to PUT updates to
    an existing task and to DELETE it.
    
- models - contain classes to verify and send to a db.
  * Task - a concrete todo with attr:
    * id - primary key
    * title - title of the task, cannot be more than 150 chars
    * content - description of the task
    * created_at - date and time when task was create
  
- create_db - uses for creating db before first run or adding new models to existing db.
  NOTE: you cannot edit existing models like that, only add new ones.
  * REGISTERED_MODELS - if you add new models add it to this list and run the module.
  
- config - project config.
  * DEBUG - set it true if you need debugging information in console. 
    Also set debug flag for a flask app.
  * TESTING - set True if you need to run test_main. Do not set true for any other purposes.
  * DATABASE_NAME - name it yourself if you want before run create_db.py. Add .db in the end
  * LOG_FILE - path and name for logfile
  
- test_main - test module for testing API paths. Before testing set config.TESTING True. 
  It allows use  in memory temp database for test cases.
  
Deployment of the app
---
You should use python > 3.9
1. Use git clone or upload zip and extract it
2. Go to a TodoGARPEX dir
3. Init python virtual env by script in TodoGARPEX/Scripts
   * for windows:  activate.bat
   * for linux: activate
4. Go to TodoGARPEX dir and use command in console  
   * for windows:
     > pip install -r requirements.txt 
   * for linux:
     > pip3 install -r requirements.txt
5. Set DEBUG and TESTING in config False\
6. Run command
   * for windows:
     > python create_db.py
   * for linux:
     > python3 create_db.py
7. Run the app.
   * for windows:
     > python main.py
   * for linux:
     > python3 main.py

NOTE: if you deploy app to a remote server you can follow this way (for linux while in root dir
with sudo permissions):
> sudo apt-get install python3-pip

> sudo apt install git

> git clone https://github.com/Rebbit13/TodoGARPEX.git

> cd TodoGARPEX
 
> export PYTHONPATH=~/TodoGARPEX/Lib/site-packages

> nohup python3 ~/TodoGARPEX/main.py > /dev/null 2>&1 &

The app will run in no screen mode

**Rebbit13**
