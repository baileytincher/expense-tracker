from app import app, db, auth
from flask import request, jsonify, g, abort, url_for, make_response
from app.models import User

import sys

@auth.verify_password
def verify_password(username_or_token, password=None):
    """
    Accepts a token or username/password and checks validity.

    First checks to see if the input is a valid token. If it is not it then
    checks to see if a valid username/password combination were input.

    Args:
        username_or_token (str): Either the serialized token or the raw username
        password (str): The user's username if a token is not being used

    Returns:
        bool: True iff there's a valid user corresponding to the args
    """

    user = User.verify_auth_token(username_or_token)

    if user is None:
        user = User.query.filter_by(username=username_or_token).first()
        if user is None or password is None or not user.verify_password(password):
            return False

    g.user = user
    print('Verified user login:', g.user, file=sys.stderr) # TODO: replace with real logs
    return True

@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')

    if username is None or password is None or email is None:
        return make_response(jsonify({'error': 'missing args'}), 400)
    elif User.query.filter_by(username=username).first() is not None:
        return make_response(jsonify({'error': 'existing user'}), 400)

    if first_name is None:
        first_name = ''

    if last_name is None:
        last_name = ''

    user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

# Only available to registered users
@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })

@app.route('/api/token')
@auth.login_required
def generate_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii')})
