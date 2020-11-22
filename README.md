## About

The project is a full-stack blog application written in Python using Flask microframework. It provides a simple blogging service and includes authentication through flask-login. The data is stored in the SQLite database. The frontend is provided through Jinja templates and WTForms.

The project was deployed and is available at [Heroku](https://flask-company-blog-app.herokuapp.com/).

## Features

The application provides features of **registering new users, logging in, updating and fetching users**, as well as **listing, adding, updating and removing posts**. It allows uploading user profile photos.

## Setup

- Clone repository
- Create virtual environment:
```
python -m venv venv
```
- Install packages from `requirements.txt`:
```
pip install -r requirements.txt
```
- Migrate database:
```
flask db upgrade
```
- Enter "Run" command:
```
flask run
```

## Technologies

Technology-wise, the app utilizes:
- Python 3.8.6
- Flask 1.1.2
- Flask-Login 0.5.0
- Jinja2 2.11.2
- WTForms 2.3.3
- Pillow 8.0.1
- Alembic 1.4.3
- SQLAlchemy 1.3.20
- SQLite database
- Bootstrap 4.0.0
