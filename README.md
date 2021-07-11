This is a test web service for todo list
---
You can create todos, reed, update, delete them within an API.

Main libraries
---
- Python 3.9.1 (you should use python > 3.9)
- Flask as a core module
- flask-restx as a module to build CRUD API
- peewee as an ORM
  
Deployment of the app via docker-compose in *nix
---
Go to the app dir (evgeniy_todo) and
run the command:
>cp ./example.env ./.env

Change environment vars if you need and then:
> sudo docker-compose up

Testing
---
Go to the app dir (evgeniy_todo) and run the commands
> pip3 install -r requirements.txt
> 
> export $(grep -v '^#' test.env | xargs)
> 
> python3 -m unittest tests/test_task.py


**Rebbit13**