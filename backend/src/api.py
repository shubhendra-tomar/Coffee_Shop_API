import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
'''
  Set up CORS. Allow '*' for origins.
'''
CORS(app, resource={r"*":{'origins':'*'}})


'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES
'''
GET /drinks
    it should be a public endpoint
    it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks 
    is the list of drinks or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.all()
        drinks_list = [drink.short() for drink in drinks]
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': drinks_list
    }), 200


'''
GET /drinks-detail
    it should require the 'get:drinks-detail' permission
    it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks or appropriate status code indicating
    reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_details(payload):
    try:
        drinks = Drink.query.all()
        drinks_list = [drink.long() for drink in drinks]
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': drinks_list
    }), 200


'''
POST /drinks
    it should create a new row in the drinks table
    it should require the 'post:drinks' permission
    it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    # load the request body
    body = request.get_json()
    req_title = body.get('title')
    if type(body.get('recipe')) == str:
        req_recipe = body.get('recipe')
    else:
        req_recipe = json.dumps(body.get('recipe')) #convert object into json
    try:
        if req_title is not None and req_recipe is not None:
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
        else:
            abort(400)
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200


'''
PATCH /drinks/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should update the corresponding row for <id>
    it should require the 'patch:drinks' permission
    it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, drink_id):
    # load the request body
    body = request.get_json()
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        #check for availability of requested drink in database
        if drink is None:
            abort(404)
        req_title = body.get('title')
        req_recipe = body.get('recipe')
        if req_title:
            drink.title = req_title
        if req_recipe:
            drink.recipe = json.dumps(req_recipe)  #to convert object into json

        drink.update()
    except Exception:
        abort(400)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200


'''
DELETE /drinks/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should delete the corresponding row for <id>
    it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink.delete()
    except Exception:
        db.session.rollback()
        abort(400)

    return jsonify({
        'success': True,
        'delete': drink_id
    }), 200


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


'''
implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
implement error handler for BadRequest
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


'''
implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400
