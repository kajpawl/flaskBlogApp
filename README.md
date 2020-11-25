## About

The project is a full-stack blog application written in Python using Flask microframework. It provides a simple blogging service and includes authentication through Flask-Login (Flask-JWT-Extended for API). The data is stored in the SQLite database. The frontend is provided through Jinja templates and WTForms.

The project was deployed and is available at [Heroku](https://flask-company-blog-app.herokuapp.com/).

## Features

The application provides features of **registering new users, logging in, updating and fetching users**, as well as **listing, adding, updating and removing posts**. It allows uploading user profile photos.

## REST API Endpoints

The API is implemented in the REST architecture. All "non-GET" routes require authentication through JWT (received through `login` endpoint). The API supports the following endpoints:

### Posts
- Get all posts:
`
GET: /api/v1/posts
`

- Get single post:
`
GET: /api/v1/posts/<id>
`

- Upload new post:
`
POST: /api/v1/posts
`  
```
{
  "title": "Post title",
  "text": "Post text"
}
```

- Edit post:
`
PUT / PATCH: /api/v1/posts/<id>
`  
```
{
  "title": "Post title",
  "text": "Post text"
}
```

- Delete post:
`
DELETE: /api/v1/posts/<id>
`


### Users
- Get all users:
`
GET: /api/v1/users
`

- Get single user:
`
GET: /api/v1/users/<username>
`

- Log in:
`
POST: /api/v1/users/login
`  
```
{
  "username": "your sername",
  "password": "your password"
}
```


- Create new user (register):
`
POST: /api/v1/users/register
`  
```
{
  "email": "sample@email.com",
  "username": "Username",
  "password": "password"
}
```

- Update user:
`
PUT / PATCH: /api/v1/users/<username>
`  
```
{
  "confirm_password": "current password",
  "email": "new email",
  "username": "new username",
  "password": "new password"
}
```

- Delete user:
`
DELETE: /api/v1/users/<username>
`

- Get your account data
`
GET: /api/v1/users/account
`  

- Get posts of a user:
`
GET: /api/v1/users/<username>/posts
`  

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
- Flask-JWT-Extended 3.25.0
- Jinja2 2.11.2
- WTForms 2.3.3
- Pillow 8.0.1
- Alembic 1.4.3
- SQLAlchemy 1.3.20
- SQLite database
- Bootstrap 4.0.0
