# DBMS-mini-project using django
Prerequisites
1. Install Python
Install python and python-pip. Follow the steps from the below reference document based on your Operating System. Reference: https://docs.python-guide.org/starting/installation/

2.Install Django
```bash
py -m pip install Django
```

# Clone git repository
https://github.com/vinaykabadagi/DBMS-Mini-Project

# Run the server
```bash
# Make migrations
python manage.py makemigrations
python manage.py migrate

# Create Super User
python manage.py createsuperuser

# Run the server
python manage.py runserver 
```
Try opening http://localhost:8000 in the browser. Now you are good to go.
