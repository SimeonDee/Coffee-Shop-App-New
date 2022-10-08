from crypt import methods
import os
from re import T
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

# ---------------------------------------
# TESTING AUTH
# ---------------------------------------

# @app.route('/auth/payload', methods=['GET'])
# @requires_auth(permission='get:drinks')
# def auth_get_payload(payload):
#     return jsonify({
#         'success': True,
#         'msg': 'Token received',
#         'payload': payload
#     })


# @app.route('/auth/callback', methods=['GET', 'POST'])
# def auth_result_callback():
#     return jsonify({
#         'success': True,
#         'msg': 'login successful'
#     })


# @app.route('/auth/logout', methods=['GET', 'POST'])
# def auth_logout():
#     return jsonify({
#         'success': True,
#         'msg': 'logged out successful'
#     })


@app.route('/drinks')
@requires_auth(permission='get:drinks')
def get_drinks(payload):
    drinks = Drink.query.all()
    if drinks == None or len(drinks) < 1:
        abort(404)

    drinks = [drink.long() for drink in drinks]
    # drinks = [drink for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth(permission='get:drinks-detail')
def get_drinks_details(payload):
    drinks = Drink.query.all()
    if drinks == None or len(drinks) < 1:
        abort(404)

    drinks = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def post_drinks(payload):
    body = request.get_json()

    if 'title' not in body and 'recipe' not in body:
        abort(422)

    title = body.get('title')
    recipe = json.dumps(body.get('recipe'))

    existing_drink = Drink.query.filter(Drink.title == title).one_or_none()

    if existing_drink is None:  # Already Existing
        abort(409)  # Conflict: Already existing record

    new_drink = Drink(title, recipe)

    new_drink.insert()

    return jsonify({
        'success': True,
        'drinks': [new_drink.long()]
    }), 201


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def update_drinks(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink == None:
        abort(404)

    body = request.get_json()

    if body is None:
        abort(400)  # bad request

    if 'title' not in body or 'recipe' not in body:
        abort(422)

    if 'title' in body:
        drink.title = body.get('title')

    if 'recipe' in body:
        drink.recipe = json.dumps(body.get('recipe'))

    drink.update()

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drinks(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink == None:
        abort(404)

    drink.delete()

    return jsonify({
        'success': True,
        'delete': drink.id
    })


# Error Handling
'''
Example error handling for unprocessable entity
'''

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(403)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": 'Forbidden. Not authorized to access resource'
    }), 403


@app.errorhandler(409)
def conflict_already_existing(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": 'Conflict. Cannot create an already existing resource'
    }), 409


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server error: We are sorry for this"
    }), 500


'''
@TODO implement error handler for 404
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
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


# @app.errorhandler(AuthError().status_code)
# def not_found(error):
#     return jsonify({
#         "success": False,
#         "error": error.status_code,
#         "message": error.error
#     }), error.status_code
