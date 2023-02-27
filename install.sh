apt-get update
apt install python3.9-venv
apt-get install libgl1

python3 -m venv ./env
source env/bin/activate

pip install   opencv-python flask flask-sqlalchemy PyMySQL cryptography uuid flask-cors datetime flask_bcrypt flask_security email_validator flask_jwt_extended opencv-python

mysql -u root -e "create database if not exists apipeople"; 
