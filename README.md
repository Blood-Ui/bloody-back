# Blood UI Backend API

This repository contains the backend API for the web application "Blood UI". The API is built using Django REST Framework (DRF).
The API has been deployed to PythonAnywhere and is accessible at [lordgrim18.pythonanywhere.com](http://lordgrim18.pythonanywhere.com/).

## Features

* **CRUD operations:** Create, Read, Update, and Delete functionalities for various web application's data models.
* **Authentication:** Implement user authentication using mechanisms like JWT.
* **Permissions:** Control access to API endpoints based on user roles or permissions.
* **Bulk operations:** Perform bulk operations on data models. For example, bulk create.
* **API documentation:** Provide API documentation for developers to understand the API endpoints and their functionalities.
* **Deployment:** Deploy the API to a cloud platform for public access.

### Prerequisites

* Python 3.x

### Installation

1. Clone this repository.
```bash
git clone https://github.com/Blood-Ui/bloody-back.git
```
2. Create a virtual environment and activate it.
```bash
python -m venv venv
venv/bin/activate
```
3. Install dependencies.
```bash
pip install -r requirements.txt
```

### Configuration

1. Copy .env.sample to .env and update the configuration values.
2. Update .env file with your database configuration, secret keys, and other project-specific details.

### Database Migrations

**Initial Setup:**

1. Run `python manage.py makemigrations` to generate migration files for your data models.

2. Run `python manage.py migrate` to create database tables based on the migrations.

**Note:** Currently, Django's default migration commands are used. We plan to implement custom migrations in the future for greater control over the database schema.

### Running the API

**Development Server:**

1. Run `python manage.py runserver` to start the development server.
2. The API will be accessible at http://127.0.0.1:8000/ by default (port may vary).

**Deployed API:**

* Access the deployed API at [lordgrim18.pythonanywhere.com](http://lordgrim18.pythonanywhere.com/).

### API Documentation

Contact the project maintainers to obtain the API documentation. A Postman collection will be provided for testing the API endpoints.

### Contributing

We welcome contributions to this project! Please contact the maintainers for further details.