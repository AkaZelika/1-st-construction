from flask import Flask, render_template, request, redirect, url_for, session
import database
from werkzeug.utils import secure_filename
import os

app = Flask("__name__")
app.secret_key = "trekjse654hlwdkhfoscvnourhgmxbkruthowednfrh0w3948yv65thde3455v6dekruitfos"

UPLOAD_FOLDER = "static\products"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def create_session():
    pattern = session.get("user", {})
    if not pattern:
        pattern = {"data":{"key":0}, "cart":{"product":{}, "ticket":{}}}
        session["user"] = pattern
    return pattern

@app.route("/")
def timetable():
    pattern = session.get("user", {})
    if not pattern:
        pattern = {"data":{"key":0}, "cart":{"product":{}, "ticket":{}}}
        session["user"] = pattern
    print(1, session.get("user", {}))
    print(2, session.get("user", {})["data"])
    print(3, session.get("user", {})["cart"])
    concerts = database.get_concerts()
    return render_template("timetable.html", concerts=concerts, admin=pattern["data"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        admin = ["romanche0800@gmail.com"]
        errors = []
        pattern = session.get("user", {"data":{}, "cart":{"product":{}, "ticket":{}}})
        type_login = request.form["type"]
        email = request.form["email"]
        if len(errors)==0:
            if type_login=="login":
                user_data = database.get_user(email, info="id, city")
                pattern["data"]["id"] = user_data[0]
                pattern["data"]["email"] = email
                pattern["data"]["city"] = user_data[1]
                if email in admin:
                    pattern["data"]["key"] = 1
                else:
                    pattern["data"]["key"] = 0
            else:
                city = request.form["city"]
                database.user_login(email, city)
                pattern["data"]["id"] = database.get_user(email, info="id")
                pattern["data"]["email"] = email
                pattern["data"]["city"] = city
            session["user"] = pattern
            return render_template("timetable.html", admin=session.get("user", {})["data"]["key"])
        else:
            return render_template("userlogin.html", errors=errors)
    else:
        return render_template("userlogin.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("timetable"))

@app.route("/shop")
def shop():
    cart = session.get("user", {})["cart"]["product"]
    in_cart = []
    for id in cart:
        in_cart.append(database.get_cart_product(cart[id])[2])
    products = database.get_items()
    return render_template("shop.html", products=products, in_cart=in_cart, admin=session.get("user", {})["data"]["key"])

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

        database.add_item(name=name, price=price, image=image_path, description=description, count=count)
        print("save")
        return redirect(url_for("shop"), admin=session.get("user", {})["data"]["key"])
    else:
        return render_template("addproduct.html", admin=session.get("user", {})["data"]["key"])
    
@app.route("/product/<product_name>/<int:product_id>")
def product(product_name, product_id):
    cart = session.get("user", {})["cart"]["product"]
    for id in cart:
        count = database.product_in_cart(cart[id], product_id)
        print(count)
    product_info = database.get_item(product_id, product_name)
    return render_template("productinfo.html", product_info=product_info, count=count, admin=session.get("user", {})["data"]["key"])
    
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    user = session.get("user", {})
    user_id = user["data"]["id"]
    cart = user["cart"]["product"]
    
    cart[len(cart)+1] = database.buy_product(user_id, product_id)
    session["user"] = user
    return redirect(url_for("shop"))

@app.route("/ticket/<int:ticket_id>")
def buy_ticket(ticket_id):
    ticket_info = database.get_ticket(int(ticket_id))
    return render_template("buyticket.html", ticket_info=ticket_info, admin=session.get("user", {})["data"]["key"])

@app.route("/add_concert", methods=["GET", "POST"])
def add_concert():
    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]
        city = request.form["city"]
        location = request.form["location"]
        count_ticket = request.form["count_ticket"]
        database.add_concert(date, time, city, location, count_ticket)
        return redirect(url_for("timetable"))
    else:
        return render_template("addconcert.html", admin=session.get("user", {})["data"]["key"])

app.run(debug=True)