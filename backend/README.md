# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```     

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

There are 5 end points configured for application functionality in `api.py` file.

1. `/drinks` : 
        `Method used` : get
        `use` : this end point returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks in short format or appropriate status code indicating reason for failure.

2. `/drinks-detail` : 
        `Method used` : get
        `use` : this end point returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks in long format with its ingredients and their quantity or appropriate status code indicating reason for failure

3. `/drinks` : 
        `Method used` : post
        `use` : this end point accepts recipe details from user and inserts them into DB and returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink or appropriate status code indicating reason for failure

4. `/drinks/<id>` : 
        `Method used` : patch
        `use` : this end point accepts id of drink which is to be updated, updated details and uses it to update drink's details and returns status code 200 and json {"success": True, "drinks": drink} where drink is an array containing only the updated drink or appropriate status code indicating reason for failure

5. `/drinks/<id>` : 
        `Method used` : delete
        `use` : this end point accepts id of the drink which is to be deleted and returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record or appropriate status code indicating reason for failure

In `auth.py` file multiple functions are implemented for Authorisation and request checks. Following validations are implemented in given file :

1. `get_token_auth_header` function is implemented for request validation and token availability.
2. `check_permissions` function is implemented for checking permissions for user.
3. `verify_decode_jwt` function is implemented for token check. 