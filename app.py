from flask import Flask, render_template, request, redirect, url_for
import database
from werkzeug.utils import secure_filename
import os

app = Flask("__name__")

UPLOAD_FOLDER = "static/products"
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
        print(date, time, city, location, count_ticket)
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

        database.app_item(name=name, price=price, image=image_path, description=description, count=count)
        return redirect(url_for("shop"))
    else:
        return render_template("addproduct.html")

app.run(debug=True)