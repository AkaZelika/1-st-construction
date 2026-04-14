from flask import Flask, render_template

app = Flask("__name__")

@app.route("/")
def timetable():
    return render_template("timetable.html")

app.run(debug=True)