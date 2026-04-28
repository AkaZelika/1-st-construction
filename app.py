from flask import Flask, render_template, request, redirect, url_for, session
import database
from werkzeug.utils import secure_filename
import os

app = Flask("__name__")
app.secret_key = "trekjse654hlwdkhfoscvnourhgmxbkruthowednfrh0w3948yv65thde3455v6dekruitfos"

UPLOAD_FOLDER = "static\products"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def timetable():
    concerts = database.get_concerts()
    return render_template("timetable.html", concerts=concerts)

@app.route("/ticket/<int:ticket_id>")
def buy_ticket(ticket_id):
    ticket_info = database.get_ticket(int(ticket_id))
    return render_template("buyticket.html", ticket_info=ticket_info)

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
        return render_template("addconcert.html")
    
@app.route("/shop")
def shop():
    products = database.get_items()
    return render_template("shop.html", products=products)

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
        return redirect(url_for("shop"))
    else:
        return render_template("addproduct.html")
    
@app.route("/product/<product_name>/<int:product_id>")
def product(product_name, product_id):
    product_info = database.get_item(product_id, product_name)
    return render_template("productinfo.html", product_info=product_info)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        #user = session.get("user", {})
        errors = []
        data = {}
        type_login = request.form["type"]
        email = request.form["email"]
        city = request.form["city"]
        if len(errors)==0:
            if type_login=="login":
                user_data = database.get_user(email, info="id, city")
                data["id"] = user_data[0]
                data["email"] = email
                data["city"] = user_data[1]
            else:
                database.user_login(email, city)
                data["id"] = database.get_user(email, info="id")
                data["email"] = email
                data["city"] = city
            session["user"] = data
            return render_template("timetable.html", errors=errors)
        else:
            return render_template("userlogin.html", errors=errors)
    else:
        return render_template("userlogin.html")
    
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    user_id = session.get("user", {})["data"]["id"]
    user_cart = session.get("user", {})["cart"]
    new_product = database.buy_product(user_id, product_id)
    if user_cart:
        user_cart[str(new_product[0])] = 1
    else:
        ...
    return redirect(url_for("shop"))

app.run(debug=True)