from database.db import db
from models.models import Manager, User, Categories, Products, Cart, Sales, Purchases
import hashlib
import re
import random 
from matplotlib.figure import Figure
import numpy as np
import io
import base64
from datetime import datetime

# Authentication and Validation helpers
def encrypt(password):
    ''' ShA256 '''
    hash_pass = hashlib.sha256()
    hash_pass.update(password.encode("utf-8"))
    return str(hash_pass.digest())

def checkAuthentication(ref, uname, password):
    ''' Same function for user and manager '''
    if ref == 'manager':
        manager = db.session.query(Manager).filter(Manager.username == uname, Manager.password == password).first()
        #manager = db.session.query(Manager).all()
        #print(manager.username)
        if manager == None:
            return False
    else:
        password = encrypt(password)
        user = db.session.query(User).filter(User.username == uname, User.password == password).first()
        if user == None:
            return False
    return True

def validateInput(uname,email,password,confirm):
    if len(uname) == 0 or len(email) == 0 or len(password) == 0 or len(confirm) == 0:
        return 'Please fill all the fields'
    if password != confirm:
        return 'Password must match with confirm password'
    if len(password) < 8:
        return 'Length of password must be greater than or equal to 8'
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex,email):
        return 'Enter valid email'
    return 'true'

# Manager helpers
def summaryGeneration():
    products = db.session.query(Sales).all()
    categories = {}
    for i in products:
        if i.category_id in categories:
            categories[i.category_id][1] += i.sale
        else:
            print(i.category_id)
            temp = db.session.query(Categories).filter(Categories.category_id == i.category_id).first()
            if temp != None:
                temp = temp.name
            else:
                continue
            categories[i.category_id] = [temp, i.sale]
    temp = list(categories.values())
    return temp

def plotGeneration():
    # https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
    categories = summaryGeneration()
    fig = Figure()
    axis = fig.add_subplot(1 ,1 ,1)
    x = [i[0] for i in categories]
    y = [i[1] for i in categories]
    axis.bar(x, y)
    out = io.BytesIO()
    fig.savefig(out, format="png")
    img = base64.b64encode(out.getbuffer()).decode("ascii")
    return img

# Category helpers
def newCategory(name):
    le = int(random.random()*10000000)+random.randint(1,100)
    le = name[0]+str(le)+name[-1]
    name = name.strip()
    if len(name) < 1:
        return "Enter valid name"
    sname = name.lower()
    try:
        db.session.add(Categories(category_id = le,name = name,search = sname))
        db.session.commit()
    except:
        return "Enter valid details"
    else:
        return "true"

def updateCategory(name,id):
    name = name.strip()
    if len(name) < 1:
        return "Enter valid name"
    sname = name.lower()
    try:
        db.session.query(Categories).filter(Categories.category_id == id).update({"name":name,"search":sname})
        db.session.commit()
    except:
        return "Enter valid details"
    else:
        return "true"
    
def removeCategory(id):
    try:
        db.session.query(Products).filter(Products.category_id == id).delete()
        db.session.query(Categories).filter(Categories.category_id == id).delete()
        db.session.commit()
    except:
        return False
    else:
        return True

def getCategories():
    categories = db.session.query(Categories).all()
    #categories = [cat.name for cat in categories]
    return categories

# Product helpers
def getProducts():
    # Gives all the products in a list with respective category_id as key in dictionary
    categories = getCategories()
    products = {}
    for i in categories:
        products[i] = db.session.query(Products).filter(Products.category_id == i.category_id).all()
    return products

def getaProduct(prod_id):
    return db.session.query(Products).filter(Products.product_id == prod_id).first()

def newProduct(cat_id,name,price,unit,stock,fractal):
    name = name.strip()
    if len(name) < 1:
        return False
    sname = name.lower()
    prods = db.session.query(Products).all()
    le = int(random.random()*10000000)+random.randint(1,100)
    le = name[0]+str(le)+name[-1]
    try:
        price = float(price)
        stock = float(stock)
    except:
        try:
            price = float(price)
            return "Enter valid stock."
        except:
            return "Enter valid price."
    if price <= 0 or stock <= 0:
        return "Enter valid price/stock"
    new_product = Products(product_id = le,category_id = cat_id,name = name,price = price,unit = unit,stock = stock,fractal_allowed = fractal, search = sname)
    try:
        db.session.add(new_product)
        db.session.commit()
    except:
        return "Enter valid category"
    else:
        return "true"
    
def updateProduct(prod_id,cat_id,changed_name,price,unit,stock,fractal):
    changed_name = changed_name.strip()
    if len(changed_name) < 1:
        return False
    sname = changed_name.lower()
    try:
        price = float(price)
        stock = float(stock)
    except:
        try:
            price = float(price)
            return "Enter valid stock."
        except:
            return "Enter valid price."
    if price <= 0 or stock <= 0:
        return "Enter valid price/stock"
    try:
        db.session.query(Products).filter(Products.category_id == cat_id,Products.product_id == prod_id).update({"name":changed_name,"price":price,"unit":unit,"stock":stock,"fractal_allowed":fractal,"search":sname})
        db.session.commit()
    except:
        return "Enter valid details"
    else:
        return "true"

def removeProduct(cat_id, prod_id):
    ''' Deleting product by manager '''
    try:
        db.session.query(Products).filter(Products.category_id == cat_id, Products.product_id == prod_id).delete()
        db.session.commit()
    except:
        return False
    else:
        return True

# User helpers
def newUser(uname,password,email):
    ''' User registration '''
    users = db.session.query(User).all()
    le = len(users)+1
    try:
        new_user = User(user_id = le, username = uname, email = email, password = encrypt(password))
        db.session.add(new_user)
        db.session.commit()
    except:
        return False
    else:
        return True

def addToCart(user_id,prod_id):
    ''' Single quantity added to cart
    Before adding cart is checked first and no changes are made if product already exists'''
    product = db.session.query(Products).filter(Products.product_id == prod_id).first()
    temp = db.session.query(Cart).filter(Cart.user_id == user_id,Cart.product_id == prod_id).first()
    if temp != None:
        return False
    else:
        le = prod_id[:3]+str(int(random.random()*10000000)+random.randint(1,100))
        db.session.add(Cart(cart_id=le,user_id=user_id,product_id = prod_id,quantity=1,unit=product.unit,price = product.price))
        db.session.commit()
        return True

def buyNow(user_id,prod_id,quantity):
    try:
        quantity = float(quantity)
    except:
        return "Enter valid quantity"
    product = db.session.query(Products).filter(Products.product_id == prod_id).first()
    temp = db.session.query(Cart).filter(Cart.user_id == user_id,Cart.product_id == prod_id).first()
    check_avail = db.session.query(Cart).filter(Cart.product_id == prod_id).all()
    if quantity != int(quantity):
        if product.fractal_allowed == 'No':
            return "Quantity has to be purchased in whole, partials are not provided."
    if quantity <= 0:
        return "Enter valid quantity"
    stock_sum = 0
    for i in check_avail:
        stock_sum += i.quantity
    cost = product.price * quantity
    if temp != None:
        tempQuantity = temp.quantity
        if product.stock + tempQuantity < (stock_sum + quantity):
            print('Product not added')
            return "Enough stock is not available"
    if temp != None:
        db.session.query(Cart).filter(Cart.product_id == prod_id,Cart.user_id == user_id).update({"user_id":user_id,"product_id":prod_id,"quantity":quantity,"unit":product.unit,"price":cost})
        db.session.commit()
    else:
        le = prod_id[:3]+str(int(random.random()*10000000)+random.randint(1,100))
        if quantity > product.stock:
            return "Enough stock is not available"
        db.session.add(Cart(cart_id=le,user_id=user_id,product_id = prod_id,quantity=quantity,unit=product.unit,price = cost))
        db.session.commit()
    return "true"

def getUserCart(user_id):
    ''' Items of user with user_id in cart table '''
    products = db.session.query(Cart).filter(Cart.user_id == user_id).all()
    total = 0
    for i in products:
        total += i.price
    print(products)
    return [products, total]

def getCartItem(user_id,prod_id):
    cartid = db.session.query(Cart).filter(Cart.user_id == user_id,Cart.product_id == prod_id).first()
    return cartid

def deleteapurchase(cart_id):
    try:
        db.session.query(Cart).filter(Cart.cart_id == cart_id).delete()
        db.session.commit()
    except:
        return False
    return True

def updatePurchase(cart_id,quantity):
    try:
        db.session.filter(Cart.cart_id == cart_id).update({'quantity':float(quantity)})
        db.session.commit()
    except:
        return False
    return True

def updateStock(product_id, newStock):
    ''' Called from sold to update stock of a product '''
    try:
        db.session.query(Products).filter(Products.product_id == product_id).update({'stock':newStock})
        db.session.commit()
    except:
        return False
    else:
        return True

def sold(user_id):
    ''' Final purchase by user from cart by clicking Buy button. 
    Changes are made to sales table(adding new sale), products table(decreasing product stock) and cart(removing user and his/her purchases from cart)'''
    temp = getUserCart(user_id)
    prods = temp[0]
    total = temp[1]
    trans_id = user_id[:3]+str(int(random.random()*10000000)+random.randint(1,100) + int(total))
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    db.session.add(Purchases(transaction_id = trans_id, user_id = user_id, price = total, date = date))
    db.session.commit()
    products = []
    for i in range(len(prods)):
        products.append(getaProduct(prods[i].product_id))
        prevStock = products[i].stock - prods[i].quantity
        updateStock(prods[i].product_id, prevStock)
        temp = db.session.query(Sales).filter(Sales.product_id == products[i].product_id).first()
        if temp == None:
            db.session.add(Sales(product_id = products[i].product_id, category_id = products[i].category_id, quantity = prods[i].quantity, sale = prods[i].price))
            db.session.commit()
        else:
            db.session.query(Sales).filter(Sales.product_id == products[i].product_id).update({'quantity' : (temp.quantity + prods[i].quantity), 'sale' : (temp.sale + prods[i].price)})
            db.session.commit()
    db.session.query(Cart).filter(Cart.user_id == user_id).delete()
    db.session.commit()

def getPurchases(user_id):
    ''' Data retrieval from purchases table for user profile '''
    purchases = db.session.query(Purchases).filter(Purchases.user_id == user_id).all()
    return purchases