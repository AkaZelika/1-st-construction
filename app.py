from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask("__name__")

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

app.run(debug=True)