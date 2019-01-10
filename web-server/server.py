from app import app, db
from app.models import User

import os
if not os.path.exists('db.sqlite'):
        db.create_all()
