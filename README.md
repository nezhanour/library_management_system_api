# Library Management System API

This project is a Django-based API for managing library operations, including user management, book management, and loan tracking. It allows users to register, check out, and return books while keeping track of the availability and loan history of each book.

## Features

- **User Management**: Register, update, and delete user accounts.
- **Book Management**: Add, update, and remove books, and track their availability.
- **Loan Management**: Check out and return books with full loan history tracking.
- **Search and Filter**: Search books by title, author, or availability.

## Technologies Used

- **Django**: Main web framework.
- **Django REST Framework (DRF)**: For building the API.
- **MySQL**: Database used for storing user, book, and loan data.
- **PythonAnywhere**: Deployment platform.

## Setup Instructions

1. Clone the repository:
   git clone https://github.com/nezhanour/library_management_system_api.git

2. Navigate to the project folder:
   cd library_management_system_api

3. Create and activate a virtual environment:
   python -m venv env
   source env/bin/activate # For Linux/macOS
   '# .\env\Scripts\activate # For Windows

4. Install dependencies:
   pip install -r requirements.txt

5. Run the development server:
   python manage.py runserver
