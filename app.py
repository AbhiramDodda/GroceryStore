from flask import Flask, render_template, request, redirect, url_for, session
from database.db import db
import os
from flask_restful import Api
from Helpers.helpers import checkAuthentication, validateInput, getCategories, getProducts, newUser, getaProduct, addToCart, buyNow, getUserCart, getCartItem, sold, plotGeneration, getPurchases
from API.api import addCategory, editCategory, deleteCategory, addProduct, editProduct, deleteProduct, editPurchase, deletePurchase, search 

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:\Web\MAD1\GroceryStore\database\database.sqlite3"
    db.init_app(app)
    app.app_context().push()
    app.secret_key = os.urandom(24)
    api = Api(app)
    return app,api

app,api = create_app()

# Controllers
# Common routes
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/logout')
def logout():
    session.pop('user')
    session.clear()
    return render_template('home.html')

# Manager routes
@app.route('/manager')
def manager():
    return render_template("managerlogin.html")

@app.route('/managerlogin',methods = ['GET','POST'])
def managerlogin():
    if request.method == 'POST' and request.form['username'] != None and request.form['password'] != None:
        username = request.form['username']
        password = request.form['password']
        if checkAuthentication('manager',username,password):
            session['user'] = username
            return redirect(url_for('managerdashboard'))
        return render_template("error.html", message="Invalid credentials", link = '/manager', where = "Login again")

@app.route('/manager_dashboard',methods = ['GET','POST'])
def managerdashboard():
    if 'user' not in session:
        return render_template('home.html')
    categories = getCategories()
    products = getProducts()
    print(products)
    return render_template("managerdashboard.html", length = len(categories), categories = products)

@app.route('/category/add')
def addnewCategory():
    if 'user' not in session:
        return render_template('home.html')
    return render_template("addcategory.html")

@app.route('/<string:category_id>/<string:category_name>/editcategory')
def editaCategory(category_id,category_name):
    if 'user' not in session:
        return render_template('home.html')
    return render_template("editcategory.html",category_id = category_id,category_name = category_name)

@app.route('/<string:category_id>/deletecategory')
def deleteaCategory(category_id):
    if 'user' not in session:
        return render_template('home.html')
    return render_template("categoryconfirm.html",category_id = category_id)

@app.route('/<string:category_id>/addproduct')
def addnewProduct(category_id):
    if 'user' not in session:
        return render_template('home.html')
    return render_template("addproduct.html",category_id = category_id)

@app.route('/<string:product_id>/<string:category_id>/editproduct')
def editaProduct(product_id,category_id):
    if 'user' not in session:
        return render_template('home.html')
    prod = getaProduct(product_id)
    return render_template("editproduct.html",category_id = category_id,product_id = product_id,product = prod)

@app.route('/<string:product_id>/<string:category_id>/deleteproduct')
def deleteaProduct(product_id,category_id):
    if 'user' not in session:
        return render_template('home.html')
    prod = getaProduct(product_id)
    return render_template("productconfirm.html",category_id = category_id,product_id = product_id,product = prod)

@app.route('/manager_dashboard/summary')
def summary():
    res = plotGeneration()
    return render_template("managersummary.html", image_data = res)

# User routes
@app.route('/user')
def user():
    return render_template("userlogin.html")

@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if request.method == 'POST' and request.form['username'] != None and request.form['password'] != None:
        username = request.form['username']
        password = request.form['password']
        if checkAuthentication('user',username,password):
            session['user'] = username
            return redirect(url_for('userdashboard'))
        return render_template("error.html", message="Invalid credentials", link = '/user', where = "Login again")

@app.route('/userregister')
def userregister():
    return render_template('userregistration.html')

@app.route('/userregistration',methods=['GET','POST'])
def userregistration():
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        password=request.form['password']
        confirm_pass = request.form['confirm_password']
        result = validateInput(uname,email,password,confirm_pass)
        if  result == 'true':
            if newUser(uname,password,email):
                session['user'] = uname
                return redirect(url_for('userdashboard'))
            return render_template("error.html", message="Username exists", link = '/userregister', where = "Go back")
        return render_template("error.html", message = result, link = '/userregister', where = "Go back")

@app.route('/userdashboard')
def userdashboard():
    if 'user' not in session:
        return render_template('home.html')
    user_id = None
    if 'user' in session:
        user_id = session['user']
    else:
        return render_template("home.html")
    categories = getCategories()
    products = getProducts()
    return render_template("userdashboard.html", length = len(categories), categories = products,user_id = user_id)

@app.route('/<string:product_id>/<string:user_id>/addtocart')
def addtoCart(user_id,product_id):
    if 'user' not in session:
        return render_template('home.html')
    if addToCart(user_id,product_id):
        return redirect(url_for('userdashboard'))
    return redirect(url_for('userdashboard'))

@app.route('/<string:product_id>/<string:user_id>/buyproduct')
def buynow(product_id,user_id):
    if 'user' not in session:
        return render_template('home.html')
    product = getaProduct(product_id)
    return render_template('buyproduct.html',product = product,user_id = user_id)

@app.route('/buyproduct',methods=['GET','POST'])
def buyproduct():
    user_id = request.form['user_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    res = buyNow(user_id,product_id,quantity)
    if res == 'true':
        return redirect(url_for('userdashboard'))
    return render_template("error.html", message = res, link = '/userdashboard', where = "Go back")

@app.route('/<string:user_id>/cart')
def usercart(user_id):
    if 'user' not in session:
        return render_template('home.html')
    prods1 = getUserCart(user_id)
    prods = prods1[0]
    products = []
    for i in prods:
        products.append([i,getaProduct(i.product_id)])
    print(products)
    return render_template("usercart.html",products = products,user_id = user_id, total = prods1[1])

@app.route('/<string:user_id>/<string:product_id>/review')
def reviewpurchase(user_id,product_id):
    product = getaProduct(product_id)
    cart = getCartItem(user_id,product_id)
    #print(cart)
    return render_template("productreview.html",user_id = user_id,product = product,cart = cart)

@app.route('/<string:cart_id>/<string:product_id>/purchasedelete')
def deleteapurchase(cart_id,product_id):
    product = getaProduct(product_id)
    return render_template("purchasedelconfirm.html",cart_id = cart_id,product = product)

@app.route('/<string:user_id>/purchase')
def purchase(user_id):
    sold(user_id)
    return redirect('/userdashboard')

@app.route('/<string:user_id>/profile')
def userProfile(user_id):
    purchases = getPurchases(user_id)
    return render_template("userprofile.html",purchases = purchases,user_id = user_id)


# APIs
api.add_resource(addCategory,'/categoryapi/add')
api.add_resource(editCategory,'/categoryapi/edit')
api.add_resource(deleteCategory,'/categoryapi/delete')
api.add_resource(addProduct,'/productapi/add')
api.add_resource(editProduct,'/productapi/edit')
api.add_resource(deleteProduct,'/productapi/delete')
api.add_resource(editPurchase,'/purchaseapi/edit')
api.add_resource(deletePurchase,'/purchaseapi/delete')
api.add_resource(search,'/search')

if __name__ == "__main__":
    app.run(host='0.0.0.0')

''' Routes reference '''
''' Manager Login -> /manager -> /managerlogin -> /manager_dashboard(success)
    Manager Login -> /manager -> /managerlogin -> /manager(failure)
    User Login -> /user -> /userlogin -> /userdashboard(success)
    User Login -> /user -> /userlogin -> /user(failure)
    User Registration -> /user -> /userregister(userregistration.html) -> /userregistration -> /userdashboard(success)
    User Registration -> /user -> /userregister(userregistration.html) -> /userregistration -> /error -> /userregister(failure)
    Logout -> /logout(home.html)'''

''' New Category -> /category/add(addcategory.html) -> /categoryapi/add -> /manager_dashboard(success)
    New Category -> /category/add(addcategory.html) -> /categoryapi/add -> /error -> /manager_dashboard(failure)
    Edit Category -> /<string:category_id>/<string:category_name>/editcategory(editcategory.html) -> /categoryapi/edit -> /manager_dashboard(success)
    Edit Category -> /<string:category_id>/<string:category_name>/editcategory(editcategory.html) -> /categoryapi/edit -> /error -> /manager_dashboard(failure)
    Delete Category -> /<string:category_id>/deletecategory(categoryconfirm.html) -> /categoryapi/delete -> /manager_dashboard(success)
    Delete Category -> /<string:category_id>/deletecategory(categoryconfirm.html) -> /categoryapi/delete -> /error -> /manager_dashboard(failure)
    New Product -> /<string:category_id>/addproduct(addproduct.html) -> /productapi/add -> /manager_dashboard(success)
    New Product -> /<string:category_id>/addproduct(addproduct.html) -> /productapi/add -> /error -> /manager_dashboard(failure)
    Edit Product -> /<string:product_id>/<string:category_id>/editproduct(editproduct.html) -> /productapi/edit -> /manager_dashboard(success)
    Edit Product -> /<string:product_id>/<string:category_id>/editproduct(editproduct.html) -> /productapi/edit -> /error -> /manager_dashboard(failure)
    Delete Product -> /<string:product_id>/<string:category_id>/deleteproduct(productconfirm.html) -> /productapi/delete -> /manager_dashboard(success)
    Delete Product -> /<string:product_id>/<string:category_id>/deleteproduct(productconfirm.html) -> /productapi/delete -> /error -> /manager_dashboard(failure)
    Manager Summary -> /manager_dashboard/summary(managersummary.html)'''