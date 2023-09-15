from database.db import db
from flask_sqlalchemy import *

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, autoincrement = True)
    email = db.Column(db.String(200), nullable = False)
    username = db.Column(db.String(30),primary_key = True)
    password = db.Column(db.String, nullable = False)

class Manager(db.Model):
    __tablename__ = "managers"
    manager_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

class Categories(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)
    search = db.Column(db.String,nullable = False)

class Products(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.String, nullable = False)
    category_id = db.Column(db.String, db.ForeignKey("categories.category_id"), nullable = False)
    name = db.Column(db.String, primary_key = True, nullable = False)
    price = db.Column(db.Float, nullable = False)
    unit = db.Column(db.String, nullable = False)
    fractal_allowed = db.Column(db.String, nullable = False)
    stock = db.Column(db.Float, nullable = False)
    search = db.Column(db.String,nullable = False)

class Cart(db.Model):
    __tablename__ = "cart"
    cart_id = db.Column(db.String,primary_key = True)
    user_id = db.Column(db.String(50),nullable = False)
    product_id = db.Column(db.String, nullable = False)
    quantity = db.Column(db.String, nullable = False)
    unit = db.Column(db.String, nullable = False)
    price = db.Column(db.Float, nullable = False)

class Sales(db.Model):
    __tablename__ = "sales"
    product_id = db.Column(db.String, primary_key = True)
    category_id = db.Column(db.String, nullable = False)
    quantity = db.Column(db.String, nullable = False)
    sale = db.Column(db.Integer, nullable = False)

class Purchases(db.Model):
    __tablename__ = "purchases"
    transaction_id = db.Column(db.String, primary_key = True)
    user_id = db.Column(db.String(50),nullable = False)
    price = db.Column(db.Float, nullable = False)
    date = db.Column(db.String, nullable = False)
