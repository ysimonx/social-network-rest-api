python3 -m venv ./env
source env/bin/activate

pip install flask flask-sqlalchemy PyMySQL cryptography uuid flask-cors datetime flask_bcrypt flask_security email_validator flask_jwt_extended

mysql -u root -e "create database if not exists apipeople"; 
