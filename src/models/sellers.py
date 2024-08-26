'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from src.data.db import get_db

#Chama o banco de dados
db = get_db()

class Seller(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

'''