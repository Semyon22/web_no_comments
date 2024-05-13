from flask_sqlalchemy import SQLAlchemy
from app import app
from datetime import datetime
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///about.db"

db=SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500),nullable=True)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return f"<users {self.id}>"
