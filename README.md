# FastAPI Todo App

A multi-user Todo Management Application built using FastAPI, MySQL, SQLAlchemy, JWT Authentication, HTML, CSS, and JavaScript.

## Features

* User Registration
* User Login
* Password Hashing using bcrypt
* JWT-based Authentication
* Create Todos
* View Personal Todos
* Delete Todos
* Multi-user Support
* Input Validation
* Responsive Frontend Interface

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* Python-Jose (JWT)
* Passlib (bcrypt)

### Database

* MySQL

### Frontend

* HTML
* CSS
* JavaScript

## Project Structure

todo_app/

├── main.py

├── auth.py

├── database.py

├── models.py

├── schemas.py

├── static/

│   ├── script.js

│   └── style.css

└── templates/

```
├── register.html

├── login.html

└── dashboard.html
```

## Installation

1. Clone the repository

2. Create a virtual environment

3. Install dependencies

pip install -r requirements.txt

4. Run the application

uvicorn main:app --reload

5. Open in browser

http://127.0.0.1:8000/register-page

## Future Improvements

* Update Todo functionality in UI
* Todo completion status
* User profile management
* Docker deployment
* Role-based authorization

## Author

Reshma K
