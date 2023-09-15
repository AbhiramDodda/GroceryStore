from flask_restful import Resource
from flask import request, render_template, redirect, make_response
from Helpers.helpers import newCategory, getCategories,updateCategory, removeCategory, newProduct, getProducts, removeProduct, updateProduct, deleteapurchase, updatePurchase
from models.models import Categories, Products
from database.db import db

# Category api s
class addCategory(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        catname = request.form['category_name']
        if len(catname) == 0:
            return make_response(render_template("error.html", message="Enter valid name", link = '/manager_dashboard', where  = "Go back"))
        if newCategory(catname):
            return redirect("/manager_dashboard") # cannot import managerdashboard from app to prevent circular import
        return make_response(render_template("error.html", message="Category exists", link = '/manager_dashboard', where = "Go back")) # probable errors are category already exists
    def delete(self):
        pass

class editCategory(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        changed_name = request.form['category_name']
        if len(changed_name) == 0:
            return make_response(render_template("error.html", message="Enter valid name", link = '/manager_dashboard', where  = "Go back"))
        cat_id = request.form['category_id']
        if len(changed_name) != 0 and changed_name != 'NULL' or changed_name != 'null':
            updateCategory(changed_name,cat_id)
            return redirect('/manager_dashboard')
        return make_response(render_template("error.html", message="Category exists", link = '/manager_dashboard', where  = "Go back"))
    def delete(self):
        pass

class deleteCategory(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        choice = request.form['delete_choice']
        id = request.form['category_id']
        if choice == 'NO':
            return redirect("/manager_dashboard")  
        if removeCategory(id):
            return redirect("/manager_dashboard")
        return redirect("/error")
    def delete(self):
        pass

# Product api s
class addProduct(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        cat_id = request.form['category_id']
        prod_name = request.form['product_name']
        prod_price = request.form['product_price']
        prod_unit = request.form['product_unit']
        stock = request.form['product_stock']
        fractal = request.form['fractal_allowed']
        res = newProduct(cat_id, prod_name, prod_price, prod_unit, stock,fractal)
        if res == "true":
            return redirect("/manager_dashboard") 
        # res is either true or the message indicating illegal entry by manager
        return make_response(render_template("error.html", message = res, link = '/manager_dashboard', where  = "Go back"))
    def delete(self):
        pass

class editProduct(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        changed_name = request.form['changed_name']
        cat_id = request.form['category_id']
        prod_id = request.form['product_id']
        unit = request.form['changed_unit']
        stock = request.form['changed_stock']
        price = request.form['changed_price']
        fractal = request.form['fractal_allowed']
        if len(changed_name) != 0 and changed_name != 'NULL' or changed_name != 'null':
            res = updateProduct(prod_id,cat_id,changed_name,price,unit,stock,fractal)
            if res == 'true':
                return redirect('/manager_dashboard')
        return make_response(render_template("error.html", message = res, link = '/manager_dashboard', where  = "Go back"))
    def delete(self):
        pass

class deleteProduct(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        choice = request.form['delete_choice']
        cat_id = request.form['category_id']
        prod_id = request.form['product_id']
        if choice == 'NO':
            return redirect("/manager_dashboard")  
        if removeProduct(cat_id,prod_id):
            return redirect("/manager_dashboard")
        return redirect("/error")
    def delete(self):
        pass

# Purchase APIs
class editPurchase(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        cart_id = request.form['cart_id']
        quantity = request.form['quantity']
        if quantity < 0:
            return make_response(render_template("error.html", message = "Enter valid quantity", link = '/userdashboard', where  = "Go back"))
        if quantity > 0:
            updatePurchase(cart_id,quantity)
        elif quantity == 0:
            deleteapurchase(cart_id)
        return redirect('/userdashboard')
    def delete(self):
        pass

class deletePurchase(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        cart_id = request.form['cart_id']
        choice = request.form['confirm']
        if choice == 'Yes':
            deleteapurchase(cart_id)
        return redirect('/userdashboard')
    def delete(self):
        pass

# Search API
class search(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        search = request.form['searchvalue']
        user_id = request.form['user_id']
        search = search.lower()
        search = search.split()
        search = "".join(search)
        search = str(search)
        categorieslst = {} # list of lists of lists with list of category object and list of it's corresponding product objects appended to one outer list
        productslst = [] # list of product objects
        temp = db.session.query(Categories).all()
        for i in temp:
            if (i.search == search) or (i.search in search) or (search in i.search):
                temp1 = db.session.query(Products).filter(Products.category_id == i.category_id).all()
                categorieslst[i] = temp1
        temp = db.session.query(Products).all()
        for i in temp:
            if (i.search == search) or (i.search in search) or (search in i.search):
                productslst.append(i)
        return make_response(render_template("searchresult.html",categories = categorieslst,products = productslst,user_id = user_id))
    def delete(self):
        pass