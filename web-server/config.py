# /**
#  * https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
#  */

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

if __name__ == '__main__':
    print(Config.SECRET_KEY)
