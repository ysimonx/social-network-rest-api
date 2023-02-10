# SOCIAL NETWORK Api Rest Restfull made with Python

installer le nécessaire avec install.sh

creer une database "apipeople" sur mysql

regler run.sh pour se connecter à la bonne base

executer le flash shell pour creer les tables

>source env/bin/activate

>export DEV_DATABASE_URL=mysql+pymysql://user:password@hostnamemysql:portmysql/apipeople

>export FLASK_APP=api-people.py

>flask shell

une fois dans le shell


>from app import db

>db.create_all()

>exit()



executer le run.sh pour lancer l'api
