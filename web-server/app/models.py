from app import app, db
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import sys # TODO: Remove in production. Debugging

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(256)) # Email has max length 254
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_username(self, username):
        self.username = username

    def set_email(self, email):
        self.email = email

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        """
        Generates a user authentication token.

        Creates an auth token serialized by the SECRET_KEY in the config and
        the user's UUID.

        Args:
            expiration (int): time til expiration in seconds

        Returns:
            str: JSON serialized as auth token
        """
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({ 'id': self.id })

    # User is only known once token is decoded
    @staticmethod
    def verify_auth_token(token):
        """
        Verifies user authentication token.

        Accepts an auth token stored by the user, and then checks to see
        if the token is both valid and not expired.

        Args:
            token (str): The user token

        Returns:
            User: if valid token
            None: if valid token
        """
        # Use SECRET_KEY as Serializer
        s = Serializer(Config.SECRET_KEY)

        try:
            data = s.loads(token)
        except SignatureExpired:
            print('Expired token', token, file=sys.stderr)
            return None    # valid token, but expired
        except BadSignature:
            print('Bad token', token, file=sys.stderr)
            return None    # invalid token

        user = User.query.get(data['id'])
        return user
