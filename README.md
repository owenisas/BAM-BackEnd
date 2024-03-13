
# BAM-BackEnd

## Introduction

BAM-BackEnd is the server-side component of the BAM application, designed to handle requests, manage user data, and interact with the database securely and efficiently. This Flask-based application provides a robust API for performing a variety of operations, ensuring a seamless and responsive experience for users of the BAM application.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your system
- pip (Python package installer)
- Git (for cloning the repository)

## Installation

Follow these steps to get your development environment set up:

1. Clone the repository to your local machine:

```
git clone https://github.com/owenisas/BAM-BackEnd.git
```

2. Navigate to the project directory:

```
cd BAM-BackEnd
```

3. Install the necessary packages using `pip`:

```
pip install -r requirements.txt
```

## Setting Up the Environment Variables

To securely access the database, follow these steps to configure your environment variables:

1. Create a `.env` file in the root directory of the project.

2. Add the following lines to the `.env` file, replacing the placeholders with your actual database credentials:

```
DATABASE_URL=remote_database_connection_string
DATABASE_USER=remote_database_username
DATABASE_PASSWORD=remote_database_password
DATABASE_NAME=remote_database_name
```

3. Ensure `python-dotenv` is installed to automatically load these variables. If it's not listed in `requirements.txt`, install it via pip:

```
pip install python-dotenv
```

In your application, use the following code snippet to load and access the environment variables:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads the environment variables from the .env file

# Example of accessing an environment variable
database_url = os.getenv("DATABASE_URL")
```

## Running the Application

To run the Flask application:

1. Set the environment variable for Flask to identify the entry point of your application:

For Windows:

```
set FLASK_APP=app.py
```

For Unix/Linux/Mac:

```
export FLASK_APP=app.py
```

2. Optionally, set the Flask environment to development to enable debug mode:

For Windows:

```
set FLASK_ENV=development
```

For Unix/Linux/Mac:

```
export FLASK_ENV=development
```

3. Run the Flask application:

```
flask run
```

The application will start, and you can access it at `http://127.0.0.1:5000/`.
