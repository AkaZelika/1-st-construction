from flask import Flask, render_template, request, redirect, url_for, session
from database import *
from werkzeug.utils import secure_filename
import os

app = Flask("__name__")
app.secret_key = "trekjse654hlwdkhfoscvnourhgmxbkruthowednfrh0w3948yv65thde3455v6dekruitfos"

UPLOAD_FOLDER = "static\products"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#Создание сесии для только зашедшего пользователя
def create_session():
    pattern = session.get("user", {})
    if not pattern:
        pattern = {"data":{"key":0}, "cart":{"product":{}, "ticket":{}}}
        session["user"] = pattern
    return pattern

#Главная страница
@app.route("/")
def timetable():
    print(1, create_session())
    concerts = Database().get_concerts()
    return render_template("timetable.html", concerts=concerts, admin=create_session()["data"])

#Регестрация/вход
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        admin = ["romanche0800@gmail.com"]
        errors = []

        type_login = request.form["type"]
        email = request.form["email"]
        pattern = create_session()
        pattern["data"]["email"] = email

        if type_login=="login": 
            user = Users(email).get("id, city")
            pattern["data"]["id"] = user[0]
            pattern["data"]["city"] = user[1]
        else:
            city = request.form["city"]
            user = Users(email, city).add()
            if type(user)=="<class 'int'>":
                pattern["data"]["id"] = user
                pattern["data"]["city"] = city
            else:
                errors.append("Пользователь зарегестрирован")
        if email in admin:
            pattern["data"]["key"] = 1

        if len(errors)==0:
            session["user"] = pattern       #Добавить обновление корзины для только залогиненых
            return redirect(url_for("timetable"))
        else:
            return render_template("userlogin.html", errors=errors)
    else:
        return render_template("userlogin.html")

#Выход из сессии
@app.route("/logout")
def logout():
    session.clear()
    create_session()
    return redirect(url_for("timetable"))

#Мерч магазин
@app.route("/shop")
def shop():
    cart = session.get("user", {})["cart"]["product"]
    in_cart = []
    for id in cart:
        in_cart.append(get_cart_product(cart[id])[2])#######################################
    products = Database().get_items()
    return render_template("shop.html", products=products, in_cart=in_cart, admin=create_session()["data"])

#Добавить мерч
@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        count = request.form["count"]
        description = request.form["description"]
        image = request.files.get("image")

        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(image_path)

        Items(name=name, price=price, image=image_path, description=description, count=count).add()
        print("save")
        return redirect(url_for("shop"))
    else:
        return render_template("addproduct.html", admin=create_session()["data"])
    
#Информация о мерче
@app.route("/product/<product_name>/<int:product_id>")
def product(product_name, product_id):
    cart = session.get("user", {})["cart"]["product"]
    if cart:
        for id in cart:
            count = product_in_cart(cart[id], product_id)#######################################
    else:
        count = 0
    product_info = get_item(product_id, product_name)#######################################
    return render_template("productinfo.html", product_info=product_info, count=count, admin=create_session()["data"])

#Добавить в карзину
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    user = session.get("user", {})
    user_id = "NULL"
    if user["data"]["id"]:
        user_id = user["data"]["id"]
    cart = user["cart"]["product"]
    print(user_id, product_id, cart)
    
    cart[str(len(cart)+1)] = Carts(user_id=user_id, item_id=int(product_id)).add()
    print(cart)
    session["user"] = user
    print(user, user_id)
    return redirect(url_for("shop"))

@app.route("/cart")
def cart():
    user_cart = session.get("user", {})["cart"]
    print(user_cart)
    in_cart = {"product":{}, "ticket":{}}
    #in_cart = database.validate("cart-products", user_cart)
    for id in user_cart["product"]:
        in_cart["product"][id] = Carts(id=user_cart["product"][id]).get_info()
    print(in_cart)
    return render_template("cart.html", admin=create_session()["data"], in_cart=in_cart)

@app.route("/update_cart", methods=["POST"])
def update_cart():
    user = session.get("user", {})
    cart_id = request.form["product_id"]
    action = request.form["action"]
    count = int(request.form["count"])
    print(user["cart"]["product"][cart_id], action)
    if action=="+":
        count+=1
    else:
        count-=1
    #cart_update(cart_id, count)#######################################
    Carts(id=user["cart"]["product"][cart_id]).update(count=count)
    session["user"] = user
    return redirect(url_for("cart"))

@app.route("/delete_cart_product/<int:cart_id>")
def delete_cart_product(cart_id):
    user = session.get("user", {})
    print(user)
    for key in user["cart"]["product"]:
        if user["cart"]["product"][key]==cart_id:
            deleted = key
    del user["cart"]["product"][deleted]
    session["user"] = user
    Database().delete_cart(cart_id)
    return redirect(url_for("cart"))

#Информация о билете
@app.route("/ticket/<int:ticket_id>")
def buy_ticket(ticket_id):
    ticket_info = Database().get_concert(int(ticket_id))
    return render_template("buyticket.html", ticket_info=ticket_info, admin=create_session()["data"])

#Добавить новый концерт
@app.route("/add_concert", methods=["GET", "POST"])
def add_concert():
    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]
        city = request.form["city"]
        location = request.form["location"]
        count_ticket = request.form["count_ticket"]
        Concerts(date, time, city, location, count_ticket).add()
        return redirect(url_for("timetable"))
    else:
        return render_template("addconcert.html", admin=create_session()["data"])
    


app.run(debug=True)