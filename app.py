from flask import Flask, request, jsonify, render_template, redirect
import tinydb
import pydobot
from datetime import datetime

app = Flask(__name__)
db = tinydb.TinyDB("database.json")


@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/mover")
def form():
    return render_template("form.html")

@app.route("/move", methods=["POST"])
def robo():
    x = round(float(request.form.get("x")),2)
    y = round(float(request.form.get("y")),2)
    z = round(float(request.form.get("z")),2)
    r = round(float(request.form.get("r")),2)
    device = pydobot.Dobot(port="COM12", verbose=False)
    xi,yi,zi,ri,_,_,_,_ = device.pose()
    xi, yi, zi, ri = round(float(xi),2), round(float(yi),2), round(float(zi),2), round(float(ri),2)
    db.insert({"x": x+xi, "y": y+yi, "z": z+zi, "r": r+ri, "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    device.move_to(x + xi, yi, zi, ri, wait=True)
    device.move_to(x + xi, y + yi, zi, ri, wait=True)
    device.move_to(x + xi, y + yi, z +zi, r + ri, wait=True)
    device.close()
    return redirect("/")

@app.route("/home")
def home():
    device = pydobot.Dobot(port="COM12", verbose=False)
    device.move_to(240.53, 0, 150.23, 0, wait=True)
    device.close()
    db.insert({"x": 240.53, "y": 0, "z": 150.23, "r": 0, "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    return redirect("/")

@app.route("/logs")
def logs():
    logs = db.all()
    return render_template("logs.html", logs=logs)


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0",port=5000)