🚀 FastAPI Secure Blog API

A robust and scalable RESTful API built with FastAPI, PostgreSQL, and SQLAlchemy. This project implements full CRUD (Create, Read, Update, Delete) operations for posts, user management, and secure JWT (JSON Web Token) authentication.

✨ Key Features

FastAPI: High performance, asynchronous Python web framework.

PostgreSQL: Reliable and scalable database persistence.

SQLAlchemy ORM: Python SQL Toolkit and Object-Relational Mapper for interacting with the database.

Secure Authentication: User registration, login, and protected routes using JWT Bearer Tokens.

Password Hashing: Uses bcrypt for secure storage of user passwords.

Pydantic V2: Data validation and serialization for clear request and response schemas.

Pagination & Filtering: Supports query parameters for limiting results, skipping records, and searching by post title.

🛠️ Prerequisites

Before you begin, ensure you have the following installed on your system:

Python 3.10+

PostgreSQL (A running PostgreSQL server instance)

Git

⚙️ Setup and Installation

Follow these steps to get your development environment running.

1. Clone the Repository

git clone <your-repository-url> FastAPI1
cd FastAPI1


2. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies:

python3 -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate   # On Windows (Cmd Prompt)


3. Install Dependencies

Install all required Python packages from your requirements.txt (or install them manually):

pip install -r requirements.txt
# OR
pip install fastapi "uvicorn[standard]" psycopg2-binary sqlalchemy pydantic-settings python-jose[cryptography] bcrypt


4. Configure Environment Variables

Create a file named .env in the root of your FastAPI1 directory. This file holds your database and security credentials.

# .env

# DATABASE SETTINGS
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_db_password
DATABASE_NAME=fastapi_db
DATABASE_USERNAME=postgres

# JWT AUTHENTICATION SETTINGS
SECRET_KEY=A_VERY_LONG_AND_RANDOM_STRING_OF_CHARACTERS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


5. Start the Application

Run the application using Uvicorn. The --reload flag enables live code reloading during development.

uvicorn app.main:app --reload


The API will now be accessible at http://127.0.0.1:8000.

🧭 API Endpoints

You can explore all endpoints and test them directly using the auto-generated documentation:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

Method

Path

Description

Authentication Required

POST

/users/

Create a new user account.

No

POST

/login/

Log in and receive a JWT access token.

No

GET

/posts/

Retrieve all posts (supports limit, skip, search).

Yes

POST

/posts/

Create a new post.

Yes

GET

/posts/{id}

Retrieve a specific post by ID.

Yes

DELETE

/posts/{id}

Delete a post (only the owner can delete).

Yes

PUT

/posts/{id}

Update an existing post (only the owner can update).

Yes

📦 Project Structure

FastAPI1/
├── app/
│   ├── __init__.py
│   ├── main.py             # Main entry point (FastAPI app instance)
│   ├── config.py           # Pydantic Settings (loads .env variables)
│   ├── database.py         # SQLAlchemy connection and session handling
│   ├── models.py           # SQLAlchemy declarative models (Post, User)
│   ├── schemas.py          # Pydantic validation schemas
│   ├── oauth2.py           # JWT token generation, validation, and dependencies
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── User.py         # User CRUD operations
│   │   ├── Post.py         # Post CRUD operations
│   │   └── Auth.py         # Login route (token generation)
├── .env                    # Environment variables file
└── requirements.txt
