# mysql >  drop database apipeople; create database apipeople;use apipeople;

source env/bin/activate
export DEV_DATABASE_URL=mysql+pymysql://root@localhost:3306/apipeople
export FLASK_APP=api-people.py


flask run

# for a database delete all and create all tables, rue
# curl http://localhost:5000/api/v1/init 


