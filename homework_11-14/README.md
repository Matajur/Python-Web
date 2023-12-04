# Combined Homework of Modules 11-14


# Homework: Module 11 - Building a REST API on FastAPI

## Task

The goal of this homework is to create a REST API for storing and managing contacts. The API should be built using the FastAPI infrastructure and use SQLAlchemy for database management.

### Contacts must be stored in the database and contain the following information:

* Name
* Surname
* E-mail address
* Phone number
* Birthday
* Additional data (optional)

### The API should be able to do the following:

* Create a new contact
* Get a list of all contacts
* Get one contact per ID
* Update an existing contact
* Delete contact

### In addition to the basic CRUD functionality, the API should also have the following features:

* Contacts must be searchable by name, surname or email address (Query).
* The API should be able to retrieve a list of contacts with birthdays for the next 7 days.

## General Requirements

* Using the FastAPI framework to create APIs.
* Using ORM SQLAlchemy to work with the database.
* PostgreSQL should be used as a database.
* Support CRUD operations for contacts.
* Support for storing a contact's date of birth.
* Providing documentation for the API.
* Using the Pydantic data validation module.


# Homework: Module 12 - Authorization and Authentication

## Task

* Implement an authentication mechanism in the application;
* Implement an authorization mechanism using JWT tokens so that all operations with contacts are performed only by registered users;
* User has access only to their contacts operations.

## General Requirements

* When registering, if a user already exists with such an email, the server will return an HTTP 409 Conflict error;
* The server hashes the password and does not store it openly in the database;
* In case of successful user registration, the server must return the status of the HTTP response 201 Created and the data of the new user;
* For all POST operations of creating a new resource, the server returns the status 201 Created;
* During the POST operation, user authentication, the server accepts a request with user data (email, password) in the body of the request;
* If the user does not exist or the password does not match, an HTTP 401 Unauthorized error is returned;
* The authorization mechanism using JWT tokens is implemented by a pair of tokens: the access token access_token and the update token refresh_token.


# Homework: Module 13 - Advanced backend development topics

## Task

* Implement a mechanism for verifying the registered user's e-mail;
* Limit the number of requests to your contact routes. Be sure to limit the speed - creating contacts for the user;
* Enable CORS for your REST API;
* Implement the ability to update the user's avatar. Use the Cloudinary service.

## General Requirements

* All environment variables must be stored in an .env file. There should be no confidential data in the "clean" form inside the code;
* Docker Compose is used to run all services and databases in the application.

## Additional Task

* Implement a caching mechanism using a Redis database. Cache the current user during authorization;
* Implement a password reset mechanism for the REST API application.


# Homework: Module 14 - Testing and deployment of web applications

In this homework, continue to refine our REST API application from homework 13.

## Task

* Use Sphinx to create documentation for your homework. To do this, add docstrings to the necessary functions and class methods in the main modules.
* Cover the homework repository modules with unit tests using the Unittest framework. Take the example from the notes for the tests/test_unit_repository_notes.py module as a basis
* Functionally test any route of your choice from your homework using the pytest framework.

## Additional Task

* Cover your homework with tests more than 95%. For control, use the pytest-cov package.
