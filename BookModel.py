from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80), nullable = False)
    price= db.Column(db.Integer, nullable = False)
    author= db.Column(db.String(80), nullable = False)
    isbn= db.Column(db.Integer, nullable = False)

    def add_books(_name, _price, _author, _isbn):
        new_book = Book(name=_name, price = _price, author= _author, isbn= _isbn)
        db.session.add
