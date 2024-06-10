<h1 align = "center">
  <img src="https://i.imgur.com/HQmG6Nz.png">
</h1>

# Table of Contents
- [Introduction](#introduction) <br>
- [Requirements](#requirements) <br>
- [DB Schema Design](#db-schema-design) <br>
- [API Design](#api-design) <br>
- [Architecture and Features](#architecture-and-features) <br>
- [How to use](#how-to-use) <br>


# Introduction
The objective of the project is to build a grocery store app with one app and multiple users using Flask framework and concepts of Modern Application Development – 1. Project deals with sqlite database to store grocery store data and user data. The name of the project **SmallBasket** inspired from BigBasket.

# Requirements
|||
|--|--|
| [Python 3.11.x](https://www.python.org/) | <img src="https://i.imgur.com/SBirLsy.png" style="width:135px; height:20px;" alt="python3.11.x">|
| [flask sql-alchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/) | <img src="https://i.imgur.com/D3ITE2c.png" style="width:135px; height:20px;" alt="flasksqlalchemy">|
| [flask restful](https://flask-restful.readthedocs.io/en/latest/) | <img src="https://i.imgur.com/6I0mLHv.png" style="width:135px; height:20px;" alt="flaskrestful"> |
| [SQLite](https://www.sqlite.org/index.html) | <img src="https://i.imgur.com/zzHzq5w.png" style="width:135px; height:20px;" alt="SQLite">


# DB Schema Design
The app has SQLite named **database.sqlite3** database with 7 tables in the database folder. These tables store user and manager credentials, categories and products managers add, a table to keep track of user purchases, sales for managers and cart to keep track of user items.

|Table Name|Column Details|
|----------|--------------|
|managers|manager_id(string, primary key), username(string), password(string)|
|users|user_id(string, primary key), username(string), password(string), email(string)|
|categories|category_id(string, primary key), name(string), search(string)|
|products|product_id(string, primary key), category_id(string), name(string), search(string), price(numeric), stock(numeric), unit(string), fractal_allowed(string)|
|cart|cart_id(string, primary key), user_id(string), product_id(string_, quantity(numeric), unit(string), price(numeric)|
|sales|product_id(string, primary key), category_id(string), quantity(numeric), sale(numeric)|
|purchases|Transaction_id(string, primary key), user_id(string), price(numeric), date(string)|

# API Design
This application uses a total of 9 REST APIs to collect and process user data. All of the APIs use only **post** method as HTML does not support **put** and **delete** requests. The main tasks they take care of includes adding, editing and deleting of products and categories by managers, editing and deleting purchases of users and search feature. 

# Architecture and Features
The project starts with **start.sh** that is located in code folder(**GroceryStore folder). README file contains information on how to start the application. Database interactions are taken care by models, located in **models.py** in models folder and helper functions, located in **helpers.py** in Helpers folder. Database and **db.py** file which creates instance of SQLAlchemy reside in database folder. All the APIs reside in **api.py** of API folder. HTML and CSS files are in **templates** and **static** folders respectively. Controllers are in **app.py**

In the application only one manager exists. The manager can create categories which is empty by default, manager can add products under each category along with necessary information like stock, price etc. Manager is allowed to delete products and categories. If a non-empty category is deleted, all the products that belong to the category are also deleted. Users can see all the categories and products added by the managers in their respective dashboards. They can buy one quantity of any product by clicking **Add to cart** or add the quantity they like by selecting **Buy now**. All the products they buy among any category are displayed in cart as they are saved in cart table. In cart, they can edit and delete any purchase. 


# How to use
1. Clone this repo. <br>
- ```terminal
   git clone https://github.com/AbhiramDodda/GroceryStore
   ```
1. Install the required libraries from [Requirements](#requirements) <br>
1. Execute the python script <br>
### Admin options
1) Add Category
2) Edit Category
3) Delete Category
4) Add Products in categories
5) Edit products
6) Delete products
7) Get a summary of sales

### User options
1) View all categories with respective products added by admin
2) Purchase one quantity on one click
3) Purchase multiple quantities by specifying
4) View cart
5) Edit purchases in the cart
6) Buy products
7) View order history
8) Search for categories or products
9) Register as a new user
10) Login

All CRUD operations are handled using REST APIs built using flask-restful.
