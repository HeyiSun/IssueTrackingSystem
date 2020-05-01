# Issue Tracking System

### Environment
Django 2.2 + python3.7 + mysql

### Build
First replace the mysql account in the mysite/mysite/setting.py
```bash
cd mysite
mysql -u [username] -p < issuetracker.sql
python3.7 manage.py makemigrations
python3.7 manage.py migrate #This will insert some django table into the issuetracker schema
python3.7 manage.py runserver 8002
```
Browse to **127.0.0.1:8002/login/** and you should see a login websi
