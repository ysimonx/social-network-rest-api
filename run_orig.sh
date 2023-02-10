# drop database flaskapp; create database flaskapp;use flaskapp;

apt install python3.9-venv

source env/bin/activate
export DEV_DATABASE_URL=mysql+pymysql://user:password@hostnamemysql:portmysql/apipeople
export FLASK_APP=api-people.py
# flask shell

# >> from app import db
# >> db.create_all()
# >> exit()


flask run



