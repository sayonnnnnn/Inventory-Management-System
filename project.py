import os
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "project.db")) 

con = sqlite3.connect('C:/Users/lenovo/Documents/RDBMS-FINAL/RDBMS_PROJECT/project.db', check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sjciuse3hfens8lns'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file

db = SQLAlchemy(app)

# ---------------------  DATABASE TABLES IN THE FORM OF FLASK MODELS --------------------------------
class Gifts(db.Model):
    __tablename__ = 'gifts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Customer(db.Model):
    __tablename__ = 'customer'
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(30), primary_key=True)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(13), nullable=False, unique=True)

class Recommended(db.Model):
    __tablename__ = 'recommended'
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), primary_key=True)
    price = db.Column(db.Float, nullable=False)

# ----------------------------------------------------------------------------------------------
# ---------------------------------- ROUTING ---------------------------------------------------

@app.route("/")
def home():
    return render_template("home.html")

# COLLECTING CUSTOMER DATA
@app.route("/welcome", methods=['GET','POST'])
def welcome():
    cust = Customer.query.all()
    return render_template("welcome.html", customers = cust)

@app.route("/insert", methods=['POST'])
def insert():
    customer = Customer(name=request.form['name'], age=request.form['age'], email=request.form['email'], gender=request.form['gender'], phone=request.form['phone'])
    db.session.add(customer)
    db.session.commit()
    return redirect("/welcome")

@app.route("/clients", methods=['GET', 'POST'])
def clients():
    customers = Customer.query.all()
    return render_template("clients.html", customers=customers)

# RECOMMENDED GIFTS TO BE SHOWN USING THIS FUNCTION 
@app.route("/project", methods=['POST', 'GET'])
def rdbms():
    c = Customer.query.all()
    g = Gifts.query.all()
    if c[-1].age < 18:
        recommended_gifts_for_below18 = Gifts.query.filter(Gifts.id<20).all()
        for i in recommended_gifts_for_below18:
            cur.execute('INSERT INTO recommended(name,price) VALUES(?,?)',(i.name, i.price))
            con.commit()
    #    r = Recommended.query.all()
    #    return render_template("project.html", gifts = g, customers = c, recommended = r) 
    else:
        recommended_gifts_for_above18 = Gifts.query.filter(Gifts.id>=20).all()
        for i in recommended_gifts_for_above18:
            cur.execute('INSERT INTO recommended(name,price) VALUES(?,?)',(i.name, i.price))
            con.commit()
    r = Recommended.query.all()
    return render_template("project.html", gifts = g, customers = c, recommended = r) 

@app.route("/updateclient", methods=['POST'])
def update():
    oldName, oldAge, oldGender, oldPhone, oldEmail = request.form.get("oldName"), request.form.get("oldAge"), request.form.get("oldGender"), request.form.get("oldPhone"), request.form.get("oldEmail")
    newName, newAge, newGender, newPhone, newEmail = request.form.get("newName"), request.form.get("newAge"), request.form.get("newGender"), request.form.get("newPhone"), request.form.get("newEmail")
    s = Customer.query.filter_by(name=oldName).first()
    s.name = newName
    s.age = newAge
    s.email = newEmail
    s.gender = newGender
    s.phone = newPhone
    db.session.commit()
    return redirect("/clients")

@app.route("/deleteclient", methods=['POST'])
def delete():
    email = request.form.get("email")
    c = Customer.query.filter_by(email=email).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/project")

# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)