from flask import Flask, render_template, request
from flask import redirect, flash, url_for, escape
from flask import make_response, session
import sqlite3 as sql
from weather import get_lat_lon, get_temprature

app = Flask(__name__)
app.secret_key = "alskjfopiyweryorjoshfihaslfhuiowehriewhriowehuirowieureyriewlkdh"

def get_query(query):
    """quering database"""
    dbname = "weather.db"
    con = sql.connect(dbname)
    cursor = con.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return result



@app.route("/")
def index():
    #email = request.cookies.get("email", None)
    email = session.get("email", None)
    if email:
        result = get_query(f"SELECT * FROM user WHERE email='{email}'")[0]
        cities = get_query(f"SELECT city FROM city WHERE email='{email}'")
        cities = [ v[0] for v in cities ]
        data = []
        for city in cities:
            lat, lon = get_lat_lon(city)
            temp = get_temprature(lat, lon)
            data.append(temp)
        return render_template("weather.html", username=result[2], city=data)
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", None)
    password = request.form.get("password", None)
    if all([email, password]):
        email = email.strip().lower()
        query = f'SELECT * FROM user WHERE email="{email}"'
        result = get_query(query) # ( (1, 'sachin', 'sachin', 'sachin@gmail.com))
        if len(result)== 0:
            flash("Error! No Such Account Exists!")
            flash("Please Signup or check your login details")
            # no such user exists
        else:
            db_password = result[0][1]
            if db_password == password:
                session.update( email=email)
                return redirect(url_for("index"))
                #resp = make_response(render_template("weather.html"))
                #resp.set_cookie("email", email)
                #return resp
            else:
                flash("Error!Invalid Password Try Again!")
                # user exists check password
        #  id, name, password, email
    else:
        flash("Error! Invalid Form Data! Please Try Again")
    
    return redirect(url_for('index'))


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/mk_signup", methods=["POST"])
def mk_signup():
    name = request.form.get("name", None)
    email = request.form.get("email", None)
    password = request.form.get("password", None)
    if all([name, email, password]):
        name = name.strip().title()
        email = email.strip().lower()
        #result = get_query("SELECT * FROM user WHERE email=?", (email, ))
        try:
            con = sql.connect("weather.db")
            cursor = con.cursor()
            command = "INSERT INTO user(email, password, name) VALUES (?, ?, ?)"
            cursor.execute(command, (email, password, name))
            con.commit()
            flash("Account Sucessfully Created! Please Sign In")
            return redirect(url_for("index"))
        except sql.IntegrityError: 
            flash("Erorr! Account Already Exists! Please Sign In")
            return redirect(url_for("index"))
        except Exception: 
            flash("Erorr! Account Already Exists! Please Sign In")
            return redirect(url_for("index"))
    else:
        flash("Error! Invalid Form Data! Please Check")
        return redirect(url_for("signup"))


@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("index"))
    # resp = make_response(render_template('login.html'))
    # resp.set_cookie("email", "")
    # return resp

@app.route("/add_city", methods=["POST"])
def add_city():
    email = session.get("email", None)
    if email:
        city = escape(request.form.get("city", None)).strip().lower()
        query = f"SELECT * FROM city WHERE email='{email}' AND city='{city}'"
        result = get_query(query)
        if result:
            flash("Error!City Already Exists!")
        else:
            coords = get_lat_lon(city)
            if coords: 
                con = sql.connect("weather.db")
                cursor = con.cursor()
                cursor.execute("INSERT INTO city VALUES (?, ?)", (email, city))
                con.commit()
                cursor.close()
                con.close()
            else:
                flash("Error!Invalid City Name!City Not Found!")
        return redirect(url_for("index"))
    flash("Error!Please Login First to Add City!")

@app.route("/delete/<name>")
def delete(name):
    email = session.get("email")
    if email:
        name = name.strip().lower()
        query = f"DELETE FROM city WHERE email='{email}' AND city='{name}'"
        get_query(query)
        #flash(query)
    else:
        flash("!Need to Login First To Delete a City!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
